using Microsoft.EntityFrameworkCore;
using PressBangalore.Api.Data;
using PressBangalore.Api.Models;

namespace PressBangalore.Api.Services;

public static class DbSeeder
{
    public static async Task SeedAsync(AppDbContext db, AuthService auth)
    {
        if (await db.Users.AnyAsync()) return;

        var superAdmin = CreateUser("admin@pressbangalore.demo", "Super Admin", UserRole.SuperAdmin, auth);
        var admin = CreateUser("ops@pressbangalore.demo", "Ops Admin", UserRole.Admin, auth);
        var subAdmin = CreateUser("moderator@pressbangalore.demo", "Sub Admin", UserRole.SubAdmin, auth);
        var reporter = CreateUser("reporter@pressbangalore.demo", "Ravi Kumar", UserRole.Reporter, auth);
        var pendingReporter = CreateUser("pending@pressbangalore.demo", "Anitha S", UserRole.Reporter, auth);
        var premiumUser = CreateUser("user@pressbangalore.demo", "Priya N", UserRole.Premium, auth);
        premiumUser.IsPremium = true;

        db.Users.AddRange(superAdmin, admin, subAdmin, reporter, pendingReporter, premiumUser);

        db.ReporterProfiles.AddRange(
            new ReporterProfile
            {
                User = reporter,
                Area = "Koramangala",
                Beat = "South Bangalore",
                Languages = "en,kn",
                Status = ReporterStatus.Approved,
                ApprovedById = superAdmin.Id,
                ApprovedAt = DateTime.UtcNow.AddDays(-5)
            },
            new ReporterProfile
            {
                User = pendingReporter,
                Area = "Whitefield",
                Beat = "East Bangalore",
                Languages = "en",
                Status = ReporterStatus.Pending
            });

        var teamAlpha = new Team { Name = "Team Alpha", Region = "Bangalore South" };
        var teamBeta = new Team { Name = "Team Beta", Region = "Bangalore East" };
        db.Teams.AddRange(teamAlpha, teamBeta);

        var posts = new List<NewsPost>
        {
            MakePost(reporter, "Traffic advisory on ORR", "Heavy congestion reported near Silk Board junction.", PostType.News, "en", "https://picsum.photos/seed/pb1/800/600"),
            MakePost(reporter, "BBMP lake restoration update", "Work begins at Bellandur lake this week.", PostType.News, "kn", "https://picsum.photos/seed/pb2/800/600"),
            MakePost(reporter, "Startup funding roundup", "Three Bangalore startups raised Series A this month.", PostType.Business, "en", "https://picsum.photos/seed/pb3/800/600"),
            MakePost(reporter, "Weekend food fest", "Best street food spots in Indiranagar.", PostType.Entertainment, "en", "https://picsum.photos/seed/pb4/800/600"),
            MakeReel(reporter, "Metro expansion reel", "Quick look at new metro stations.", PostType.Professional, "en", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"),
            MakeReel(reporter, "Rain update", "Monsoon showers across the city.", PostType.News, "kn", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4"),
        };

        posts[0].Status = PostStatus.Published;
        posts[1].Status = PostStatus.Published;
        posts[2].Status = PostStatus.Published;
        posts[3].Status = PostStatus.PendingApproval;
        posts[4].Status = PostStatus.Published;
        posts[5].Status = PostStatus.Published;

        db.NewsPosts.AddRange(posts);

        db.Advertisements.AddRange(
            new Advertisement
            {
                Title = "Bangalore Coffee Festival",
                ImageUrl = "https://picsum.photos/seed/ad1/600/200",
                LinkUrl = "https://example.com",
                Slot = AdSlot.FeedTop,
                TargetCity = "Bangalore"
            },
            new Advertisement
            {
                Title = "Local Business Spotlight",
                ImageUrl = "https://picsum.photos/seed/ad2/600/200",
                LinkUrl = "https://example.com",
                Slot = AdSlot.FeedInline,
                TargetCity = "Bangalore"
            });

        var ir1 = new Investigation
        {
            IrNumber = "IR-BLR-2026-00001",
            Title = "Land encroachment inquiry",
            Description = "Investigation into reported encroachment near lake buffer zone.",
            Status = IrStatus.InProgress,
            IoUser = admin
        };
        var ir2 = new Investigation
        {
            IrNumber = "IR-BLR-2026-00002",
            Title = "Public works contract review",
            Description = "Review of road repair contract compliance.",
            Status = IrStatus.Assigned,
            IoUser = subAdmin
        };
        db.Investigations.AddRange(ir1, ir2);

        db.IRAssignments.Add(new IRAssignment
        {
            Investigation = ir1,
            Team = teamAlpha,
            Role = "Lead"
        });

        await db.SaveChangesAsync();
    }

    private static User CreateUser(string email, string name, UserRole role, AuthService auth) => new()
    {
        Email = email,
        DisplayName = name,
        Role = role,
        PasswordHash = auth.HashPassword("Demo@123"),
        City = "Bangalore",
        LanguagePref = "en"
    };

    private static NewsPost MakePost(User author, string title, string body, PostType type, string lang, string imageUrl) =>
        new()
        {
            Author = author,
            Title = title,
            Body = body,
            Type = type,
            Language = lang,
            City = "Bangalore",
            LikesCount = Random.Shared.Next(10, 500),
            ViewsCount = Random.Shared.Next(100, 5000),
            Media = [new PostMedia { Type = MediaType.Image, Url = imageUrl }]
        };

    private static NewsPost MakeReel(User author, string title, string body, PostType type, string lang, string videoUrl) =>
        new()
        {
            Author = author,
            Title = title,
            Body = body,
            Type = PostType.Reel,
            Language = lang,
            City = "Bangalore",
            DurationSec = 30,
            LikesCount = Random.Shared.Next(50, 2000),
            ViewsCount = Random.Shared.Next(500, 20000),
            Media = [new PostMedia { Type = MediaType.Video, Url = videoUrl, ThumbnailUrl = "https://picsum.photos/seed/reel/400/700" }]
        };
}
