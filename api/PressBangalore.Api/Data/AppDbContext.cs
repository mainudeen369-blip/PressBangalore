using Microsoft.EntityFrameworkCore;
using PressBangalore.Api.Models;

namespace PressBangalore.Api.Data;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<User> Users => Set<User>();
    public DbSet<ReporterProfile> ReporterProfiles => Set<ReporterProfile>();
    public DbSet<NewsPost> NewsPosts => Set<NewsPost>();
    public DbSet<PostMedia> PostMedia => Set<PostMedia>();
    public DbSet<Advertisement> Advertisements => Set<Advertisement>();
    public DbSet<Team> Teams => Set<Team>();
    public DbSet<Investigation> Investigations => Set<Investigation>();
    public DbSet<IRAssignment> IRAssignments => Set<IRAssignment>();
    public DbSet<IRReport> IRReports => Set<IRReport>();
    public DbSet<ApprovalLog> ApprovalLogs => Set<ApprovalLog>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<User>()
            .HasIndex(u => u.Email)
            .IsUnique();

        modelBuilder.Entity<ReporterProfile>()
            .HasOne(r => r.User)
            .WithOne(u => u.ReporterProfile)
            .HasForeignKey<ReporterProfile>(r => r.UserId);

        modelBuilder.Entity<Investigation>()
            .HasIndex(i => i.IrNumber)
            .IsUnique();

        modelBuilder.Entity<NewsPost>()
            .HasMany(p => p.Media)
            .WithOne(m => m.Post)
            .HasForeignKey(m => m.PostId)
            .OnDelete(DeleteBehavior.Cascade);

        foreach (var entity in modelBuilder.Model.GetEntityTypes())
        {
            foreach (var property in entity.GetProperties())
            {
                if (property.ClrType.IsEnum)
                    property.SetColumnType("varchar(32)");
            }
        }
    }
}
