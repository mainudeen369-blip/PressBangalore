namespace PressBangalore.Api.Models;

public class User
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Email { get; set; } = string.Empty;
    public string PasswordHash { get; set; } = string.Empty;
    public string DisplayName { get; set; } = string.Empty;
    public string? AvatarUrl { get; set; }
    public UserRole Role { get; set; } = UserRole.Consumer;
    public bool IsPremium { get; set; }
    public string LanguagePref { get; set; } = "en";
    public string City { get; set; } = "Bangalore";
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public ReporterProfile? ReporterProfile { get; set; }
    public ICollection<NewsPost> Posts { get; set; } = [];
    public ICollection<Investigation> InvestigationsLed { get; set; } = [];
}

public class ReporterProfile
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid UserId { get; set; }
    public User User { get; set; } = null!;
    public string Area { get; set; } = string.Empty;
    public string Beat { get; set; } = string.Empty;
    public string Languages { get; set; } = "en,kn";
    public ReporterStatus Status { get; set; } = ReporterStatus.Pending;
    public string? IdDocumentUrl { get; set; }
    public string? AppointmentLetterUrl { get; set; }
    public Guid? ApprovedById { get; set; }
    public DateTime? ApprovedAt { get; set; }
    public string? RejectionReason { get; set; }
}

public class NewsPost
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid AuthorId { get; set; }
    public User Author { get; set; } = null!;
    public string Title { get; set; } = string.Empty;
    public string Body { get; set; } = string.Empty;
    public PostType Type { get; set; } = PostType.News;
    public PostStatus Status { get; set; } = PostStatus.PendingApproval;
    public string City { get; set; } = "Bangalore";
    public string Language { get; set; } = "en";
    public int LikesCount { get; set; }
    public int ViewsCount { get; set; }
    public int? DurationSec { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public ICollection<PostMedia> Media { get; set; } = [];
}

public class PostMedia
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid PostId { get; set; }
    public NewsPost Post { get; set; } = null!;
    public MediaType Type { get; set; }
    public string Url { get; set; } = string.Empty;
    public string? ThumbnailUrl { get; set; }
}

public class Advertisement
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Title { get; set; } = string.Empty;
    public string ImageUrl { get; set; } = string.Empty;
    public string LinkUrl { get; set; } = string.Empty;
    public AdSlot Slot { get; set; } = AdSlot.FeedInline;
    public string? TargetCity { get; set; }
    public string? TargetLanguage { get; set; }
    public bool IsActive { get; set; } = true;
    public DateTime ActiveFrom { get; set; } = DateTime.UtcNow;
    public DateTime? ActiveTo { get; set; }
}

public class Team
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string Name { get; set; } = string.Empty;
    public string Region { get; set; } = string.Empty;
    public ICollection<IRAssignment> Assignments { get; set; } = [];
    public ICollection<IRReport> Reports { get; set; } = [];
}

public class Investigation
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public string IrNumber { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public IrStatus Status { get; set; } = IrStatus.Open;
    public Guid? IoUserId { get; set; }
    public User? IoUser { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public ICollection<IRAssignment> Assignments { get; set; } = [];
    public ICollection<IRReport> Reports { get; set; } = [];
}

public class IRAssignment
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid InvestigationId { get; set; }
    public Investigation Investigation { get; set; } = null!;
    public Guid TeamId { get; set; }
    public Team Team { get; set; } = null!;
    public string Role { get; set; } = "Member";
    public DateTime AssignedAt { get; set; } = DateTime.UtcNow;
}

public class IRReport
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public Guid InvestigationId { get; set; }
    public Investigation Investigation { get; set; } = null!;
    public Guid TeamId { get; set; }
    public Team Team { get; set; } = null!;
    public string ReportBody { get; set; } = string.Empty;
    public DateTime SubmittedAt { get; set; } = DateTime.UtcNow;
}

public class ApprovalLog
{
    public Guid Id { get; set; } = Guid.NewGuid();
    public ApprovalEntityType EntityType { get; set; }
    public Guid EntityId { get; set; }
    public ApprovalAction Action { get; set; }
    public Guid ActorId { get; set; }
    public string? Note { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
