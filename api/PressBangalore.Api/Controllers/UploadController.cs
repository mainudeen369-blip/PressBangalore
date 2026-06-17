using Microsoft.AspNetCore.Mvc;

namespace PressBangalore.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class UploadController(IWebHostEnvironment env, IConfiguration config) : ControllerBase
{
  private static readonly HashSet<string> Allowed = new(StringComparer.OrdinalIgnoreCase)
  {
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".mp4", ".webm", ".mp3", ".wav"
  };

  [HttpPost]
  [RequestSizeLimit(26_214_400)]
  public async Task<IActionResult> Upload(IFormFile file)
  {
    if (file.Length == 0) return BadRequest("Empty file.");

    var ext = System.IO.Path.GetExtension(file.FileName);
    if (!Allowed.Contains(ext)) return BadRequest("File type not allowed.");

    var uploadsDir = System.IO.Path.Combine(env.WebRootPath ?? System.IO.Path.Combine(env.ContentRootPath, "wwwroot"), "uploads");
    Directory.CreateDirectory(uploadsDir);

    var fileName = $"{Guid.NewGuid()}{ext}";
    var path = System.IO.Path.Combine(uploadsDir, fileName);

    await using var stream = System.IO.File.Create(path);
    await file.CopyToAsync(stream);

    var baseUrl = config["PUBLIC_URL"] ?? $"{Request.Scheme}://{Request.Host}";
    return Ok(new { url = $"{baseUrl}/uploads/{fileName}" });
  }
}

[ApiController]
[Route("api/[controller]")]
public class HealthController : ControllerBase
{
  [HttpGet]
  public IActionResult Get() => Ok(new { status = "ok", service = "PressBangalore.Api" });
}
