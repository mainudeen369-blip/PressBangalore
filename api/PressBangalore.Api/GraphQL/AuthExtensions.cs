using System.Security.Claims;
using HotChocolate.Authorization;

namespace PressBangalore.Api.GraphQL;

public static class AuthExtensions
{
    public static Guid? GetUserId(this ClaimsPrincipal user)
    {
        var sub = user.FindFirstValue(ClaimTypes.NameIdentifier)
            ?? user.FindFirstValue(ClaimTypes.Name)
            ?? user.FindFirstValue("sub");
        return Guid.TryParse(sub, out var id) ? id : null;
    }

    public static bool IsAdminRole(this ClaimsPrincipal user)
    {
        var role = user.FindFirstValue(ClaimTypes.Role);
        return role is "SuperAdmin" or "Admin" or "SubAdmin";
    }
}

public class AdminAuthorizeAttribute : AuthorizeAttribute
{
    public AdminAuthorizeAttribute() => Roles = new[] { "SuperAdmin", "Admin", "SubAdmin" };
}
