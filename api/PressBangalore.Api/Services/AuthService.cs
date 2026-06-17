using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.IdentityModel.Tokens;
using PressBangalore.Api.Models;

namespace PressBangalore.Api.Services;

public class AuthService(IConfiguration config)
{
    public string GenerateToken(User user)
    {
        var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(GetJwtSecret()));
        var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
            new Claim(JwtRegisteredClaimNames.Email, user.Email),
            new Claim(ClaimTypes.Role, user.Role.ToString()),
            new Claim("display_name", user.DisplayName)
        };

        var token = new JwtSecurityToken(
            issuer: config["Jwt:Issuer"] ?? "PressBangalore",
            audience: config["Jwt:Audience"] ?? "PressBangalore",
            claims: claims,
            expires: DateTime.UtcNow.AddDays(7),
            signingCredentials: creds);

        return new JwtSecurityTokenHandler().WriteToken(token);
    }

    public string HashPassword(string password) => BCrypt.Net.BCrypt.HashPassword(password);

    public bool VerifyPassword(string password, string hash) => BCrypt.Net.BCrypt.Verify(password, hash);

    private string GetJwtSecret() =>
        config["JWT_SECRET"] ?? config["Jwt:Secret"] ?? "PressBangalore-Demo-Secret-Change-In-Production-32chars!";
}
