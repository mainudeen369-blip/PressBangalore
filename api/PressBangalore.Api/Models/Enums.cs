namespace PressBangalore.Api.Models;

public enum UserRole
{
    Consumer,
    Premium,
    Reporter,
    SubAdmin,
    Admin,
    SuperAdmin
}

public enum ReporterStatus
{
    Pending,
    Approved,
    Rejected,
    Suspended
}

public enum PostType
{
    News,
    Reel,
    Business,
    Entertainment,
    Professional
}

public enum PostStatus
{
    Draft,
    PendingApproval,
    Published,
    Rejected
}

public enum MediaType
{
    Image,
    Video,
    Audio
}

public enum AdSlot
{
    FeedTop,
    FeedInline,
    Reels
}

public enum IrStatus
{
    Open,
    Assigned,
    InProgress,
    Consolidated,
    Closed
}

public enum ApprovalEntityType
{
    Reporter,
    Post
}

public enum ApprovalAction
{
    Approved,
    Rejected
}
