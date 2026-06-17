using System.Security.Claims;
using HotChocolate.Authorization;
using Microsoft.EntityFrameworkCore;
using PressBangalore.Api.Data;
using PressBangalore.Api.Models;
using PressBangalore.Api.Services;

namespace PressBangalore.Api.GraphQL;

public class Mutation
{
    public async Task<AuthPayload> Register(
        RegisterInput input,
        AppDbContext db,
        AuthService auth)
    {
        if (await db.Users.AnyAsync(u => u.Email == input.Email))
            throw new GraphQLException("Email already registered.");

        var user = new User
        {
            Email = input.Email.ToLowerInvariant(),
            DisplayName = input.DisplayName,
            PasswordHash = auth.HashPassword(input.Password),
            City = input.City ?? "Bangalore",
            LanguagePref = input.Language ?? "en",
            Role = UserRole.Consumer
        };
        db.Users.Add(user);
        await db.SaveChangesAsync();

        return new AuthPayload(user, auth.GenerateToken(user));
    }

    public async Task<AuthPayload> Login(
        LoginInput input,
        AppDbContext db,
        AuthService auth)
    {
        var user = await db.Users
            .Include(u => u.ReporterProfile)
            .FirstOrDefaultAsync(u => u.Email == input.Email.ToLowerInvariant())
            ?? throw new GraphQLException("Invalid email or password.");

        if (!auth.VerifyPassword(input.Password, user.PasswordHash))
            throw new GraphQLException("Invalid email or password.");

        return new AuthPayload(user, auth.GenerateToken(user));
    }

    [Authorize]
    public async Task<ReporterProfile> RegisterReporter(
        RegisterReporterInput input,
        ClaimsPrincipal claims,
        AppDbContext db)
    {
        var userId = claims.GetUserId() ?? throw new GraphQLException("Unauthorized.");
        var user = await db.Users.Include(u => u.ReporterProfile).FirstOrDefaultAsync(u => u.Id == userId)
            ?? throw new GraphQLException("User not found.");

        if (user.ReporterProfile is not null)
            throw new GraphQLException("Reporter profile already exists.");

        user.Role = UserRole.Reporter;
        var profile = new ReporterProfile
        {
            UserId = userId,
            Area = input.Area,
            Beat = input.Beat,
            Languages = input.Languages,
            IdDocumentUrl = input.IdDocumentUrl,
            Status = ReporterStatus.Pending
        };
        db.ReporterProfiles.Add(profile);
        await db.SaveChangesAsync();
        return profile;
    }

    [Authorize]
    public async Task<NewsPost> CreatePost(
        CreatePostInput input,
        ClaimsPrincipal claims,
        AppDbContext db)
    {
        var userId = claims.GetUserId() ?? throw new GraphQLException("Unauthorized.");
        var user = await db.Users.Include(u => u.ReporterProfile).FirstOrDefaultAsync(u => u.Id == userId)
            ?? throw new GraphQLException("User not found.");

        if (user.Role != UserRole.Reporter && !claims.IsAdminRole())
            throw new GraphQLException("Only reporters can create posts.");

        if (user.ReporterProfile?.Status != ReporterStatus.Approved && !claims.IsAdminRole())
            throw new GraphQLException("Reporter must be approved before posting.");

        var post = new NewsPost
        {
            AuthorId = userId,
            Title = input.Title,
            Body = input.Body,
            Type = input.Type,
            City = input.City ?? user.City,
            Language = input.Language ?? user.LanguagePref,
            DurationSec = input.DurationSec,
            Status = claims.IsAdminRole() ? PostStatus.Published : PostStatus.PendingApproval,
            Media = input.Media.Select(m => new PostMedia
            {
                Type = m.Type,
                Url = m.Url,
                ThumbnailUrl = m.ThumbnailUrl
            }).ToList()
        };
        db.NewsPosts.Add(post);
        await db.SaveChangesAsync();
        return post;
    }

    [AdminAuthorize]
    public async Task<ReporterProfile> ApproveReporter(
        Guid id,
        ClaimsPrincipal claims,
        AppDbContext db)
    {
        var profile = await db.ReporterProfiles.Include(r => r.User).FirstOrDefaultAsync(r => r.Id == id)
            ?? throw new GraphQLException("Reporter not found.");

        profile.Status = ReporterStatus.Approved;
        profile.ApprovedAt = DateTime.UtcNow;
        profile.ApprovedById = claims.GetUserId();
        profile.RejectionReason = null;

        db.ApprovalLogs.Add(new ApprovalLog
        {
            EntityType = ApprovalEntityType.Reporter,
            EntityId = profile.Id,
            Action = ApprovalAction.Approved,
            ActorId = claims.GetUserId()!.Value
        });

        await db.SaveChangesAsync();
        return profile;
    }

    [AdminAuthorize]
    public async Task<ReporterProfile> RejectReporter(
        Guid id,
        string reason,
        ClaimsPrincipal claims,
        AppDbContext db)
    {
        var profile = await db.ReporterProfiles.Include(r => r.User).FirstOrDefaultAsync(r => r.Id == id)
            ?? throw new GraphQLException("Reporter not found.");

        profile.Status = ReporterStatus.Rejected;
        profile.RejectionReason = reason;

        db.ApprovalLogs.Add(new ApprovalLog
        {
            EntityType = ApprovalEntityType.Reporter,
            EntityId = profile.Id,
            Action = ApprovalAction.Rejected,
            ActorId = claims.GetUserId()!.Value,
            Note = reason
        });

        await db.SaveChangesAsync();
        return profile;
    }

    [AdminAuthorize]
    public async Task<NewsPost> ApprovePost(Guid id, ClaimsPrincipal claims, AppDbContext db)
    {
        var post = await ApprovePostInternal(id, claims, db);
        post.Status = PostStatus.Published;
        await db.SaveChangesAsync();
        return post;
    }

    [AdminAuthorize]
    public async Task<NewsPost> RejectPost(Guid id, string reason, ClaimsPrincipal claims, AppDbContext db)
    {
        var post = await ApprovePostInternal(id, claims, db);
        post.Status = PostStatus.Rejected;

        db.ApprovalLogs.Add(new ApprovalLog
        {
            EntityType = ApprovalEntityType.Post,
            EntityId = post.Id,
            Action = ApprovalAction.Rejected,
            ActorId = claims.GetUserId()!.Value,
            Note = reason
        });

        await db.SaveChangesAsync();
        return post;
    }

    [AdminAuthorize]
    public async Task<Investigation> CreateInvestigation(
        CreateInvestigationInput input,
        IrNumberService irNumbers,
        AppDbContext db)
    {
        var ir = new Investigation
        {
            IrNumber = await irNumbers.GenerateAsync(input.CityCode ?? "BLR"),
            Title = input.Title,
            Description = input.Description,
            Status = IrStatus.Open
        };
        db.Investigations.Add(ir);
        await db.SaveChangesAsync();
        return ir;
    }

    [AdminAuthorize]
    public async Task<Investigation> AssignIo(Guid irId, Guid userId, AppDbContext db)
    {
        var ir = await db.Investigations.FindAsync(irId) ?? throw new GraphQLException("IR not found.");
        ir.IoUserId = userId;
        ir.Status = IrStatus.Assigned;
        await db.SaveChangesAsync();
        return ir;
    }

    [AdminAuthorize]
    public async Task<IRAssignment> AssignTeam(Guid irId, Guid teamId, AppDbContext db)
    {
        var assignment = new IRAssignment
        {
            InvestigationId = irId,
            TeamId = teamId,
            Role = "Member"
        };
        db.IRAssignments.Add(assignment);

        var ir = await db.Investigations.FindAsync(irId);
        if (ir is not null && ir.Status == IrStatus.Assigned)
            ir.Status = IrStatus.InProgress;

        await db.SaveChangesAsync();
        return assignment;
    }

    [AdminAuthorize]
    public async Task<Advertisement> CreateAd(CreateAdInput input, AppDbContext db)
    {
        var ad = new Advertisement
        {
            Title = input.Title,
            ImageUrl = input.ImageUrl,
            LinkUrl = input.LinkUrl,
            Slot = input.Slot,
            TargetCity = input.TargetCity,
            TargetLanguage = input.TargetLanguage,
            IsActive = true
        };
        db.Advertisements.Add(ad);
        await db.SaveChangesAsync();
        return ad;
    }

    private static async Task<NewsPost> ApprovePostInternal(Guid id, ClaimsPrincipal claims, AppDbContext db)
    {
        var post = await db.NewsPosts.FindAsync(id) ?? throw new GraphQLException("Post not found.");

        db.ApprovalLogs.Add(new ApprovalLog
        {
            EntityType = ApprovalEntityType.Post,
            EntityId = post.Id,
            Action = ApprovalAction.Approved,
            ActorId = claims.GetUserId()!.Value
        });

        return post;
    }
}

public record AuthPayload(User User, string Token);

public record RegisterInput(string Email, string Password, string DisplayName, string? City, string? Language);
public record LoginInput(string Email, string Password);
public record RegisterReporterInput(string Area, string Beat, string Languages, string? IdDocumentUrl);
public record MediaInput(MediaType Type, string Url, string? ThumbnailUrl);
public record CreatePostInput(string Title, string Body, PostType Type, string? City, string? Language, int? DurationSec, List<MediaInput> Media);
public record CreateInvestigationInput(string Title, string Description, string? CityCode);
public record CreateAdInput(string Title, string ImageUrl, string LinkUrl, AdSlot Slot, string? TargetCity, string? TargetLanguage);
