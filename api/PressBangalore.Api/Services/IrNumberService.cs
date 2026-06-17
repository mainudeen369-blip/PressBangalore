using Microsoft.EntityFrameworkCore;
using PressBangalore.Api.Data;
using PressBangalore.Api.Models;

namespace PressBangalore.Api.Services;

public class IrNumberService(AppDbContext db)
{
    public async Task<string> GenerateAsync(string cityCode = "BLR")
    {
        var year = DateTime.UtcNow.Year;
        var prefix = $"IR-{cityCode}-{year}-";

        var last = await db.Investigations
            .Where(i => i.IrNumber.StartsWith(prefix))
            .OrderByDescending(i => i.IrNumber)
            .Select(i => i.IrNumber)
            .FirstOrDefaultAsync();

        var seq = 1;
        if (last is not null && int.TryParse(last[(prefix.Length)..], out var n))
            seq = n + 1;

        return $"{prefix}{seq:D5}";
    }
}
