using System.Security.Claims;
using HotChocolate.Authorization;
using Microsoft.EntityFrameworkCore;
using PressBangalore.Api.Data;
using PressBangalore.Api.Models;

namespace PressBangalore.Api.GraphQL;

public class Query
{
    [Authorize]
    public async Task<User?> Me(ClaimsPrincipal claims, AppDbContext db) =>
        await db.Users
            .Include(u => u.ReporterProfile)
            .FirstOrDefaultAsync(u => u.Id == claims.GetUserId());

    public async Task<List<NewsPost>> Feed(
        AppDbContext db,
        string? city,
        string? language,
        int limit = 20) =>
        await db.NewsPosts
            .Include(p => p.Author)
            .Include(p => p.Media)
            .Where(p => p.Status == PostStatus.Published && p.Type != PostType.Reel)
            .Where(p => city == null || p.City == city)
            .Where(p => language == null || p.Language == language)
            .OrderByDescending(p => p.CreatedAt)
            .Take(limit)
            .ToListAsync();

    public async Task<List<NewsPost>> Reels(AppDbContext db, int limit = 20) =>
        await db.NewsPosts
            .Include(p => p.Author)
            .Include(p => p.Media)
            .Where(p => p.Status == PostStatus.Published && p.Type == PostType.Reel)
            .OrderByDescending(p => p.CreatedAt)
            .Take(limit)
            .ToListAsync();

    public async Task<NewsPost?> Post(Guid id, AppDbContext db) =>
        await db.NewsPosts
            .Include(p => p.Author)
            .Include(p => p.Media)
            .FirstOrDefaultAsync(p => p.Id == id);

    public async Task<List<Advertisement>> Ads(AppDbContext db, string? city) =>
        await db.Advertisements
            .Where(a => a.IsActive && (a.TargetCity == null || a.TargetCity == city))
            .OrderByDescending(a => a.ActiveFrom)
            .ToListAsync();

    public async Task<Investigation?> TrackIr(string irNumber, AppDbContext db) =>
        await db.Investigations
            .Include(i => i.IoUser)
            .Include(i => i.Assignments).ThenInclude(a => a.Team)
            .Include(i => i.Reports).ThenInclude(r => r.Team)
            .FirstOrDefaultAsync(i => i.IrNumber == irNumber);

    [AdminAuthorize]
    public async Task<List<ReporterProfile>> ReportersPending(AppDbContext db) =>
        await db.ReporterProfiles
            .Include(r => r.User)
            .Where(r => r.Status == ReporterStatus.Pending)
            .OrderBy(r => r.User.CreatedAt)
            .ToListAsync();

    [AdminAuthorize]
    public async Task<List<NewsPost>> PostsPendingApproval(AppDbContext db) =>
        await db.NewsPosts
            .Include(p => p.Author)
            .Include(p => p.Media)
            .Where(p => p.Status == PostStatus.PendingApproval)
            .OrderByDescending(p => p.CreatedAt)
            .ToListAsync();

    [AdminAuthorize]
    public async Task<DashboardStats> DashboardStats(AppDbContext db) => new()
    {
        TotalUsers = await db.Users.CountAsync(),
        PendingReporters = await db.ReporterProfiles.CountAsync(r => r.Status == ReporterStatus.Pending),
        PendingPosts = await db.NewsPosts.CountAsync(p => p.Status == PostStatus.PendingApproval),
        PublishedPosts = await db.NewsPosts.CountAsync(p => p.Status == PostStatus.Published),
        OpenInvestigations = await db.Investigations.CountAsync(i => i.Status != IrStatus.Closed),
        EarningsSeries = Enumerable.Range(0, 7).Select(i => new EarningsPoint
        {
            Day = DateTime.UtcNow.Date.AddDays(-6 + i).ToString("ddd"),
            Amount = 1200 + Random.Shared.Next(0, 800)
        }).ToList()
    };

    [AdminAuthorize]
    public async Task<List<Investigation>> Investigations(AppDbContext db) =>
        await db.Investigations
            .Include(i => i.IoUser)
            .Include(i => i.Assignments).ThenInclude(a => a.Team)
            .OrderByDescending(i => i.CreatedAt)
            .ToListAsync();

    [AdminAuthorize]
    public async Task<List<Team>> Teams(AppDbContext db) =>
        await db.Teams.OrderBy(t => t.Name).ToListAsync();

    [AdminAuthorize]
    public async Task<List<User>> AdminUsers(AppDbContext db) =>
        await db.Users
            .Where(u => u.Role == UserRole.Admin || u.Role == UserRole.SubAdmin || u.Role == UserRole.SuperAdmin)
            .OrderBy(u => u.DisplayName)
            .ToListAsync();

    [AdminAuthorize]
    public async Task<List<Advertisement>> AllAds(AppDbContext db) =>
        await db.Advertisements.OrderByDescending(a => a.ActiveFrom).ToListAsync();
}

public class DashboardStats
{
    public int TotalUsers { get; set; }
    public int PendingReporters { get; set; }
    public int PendingPosts { get; set; }
    public int PublishedPosts { get; set; }
    public int OpenInvestigations { get; set; }
    public List<EarningsPoint> EarningsSeries { get; set; } = [];
}

public class EarningsPoint
{
    public string Day { get; set; } = string.Empty;
    public decimal Amount { get; set; }
}
