using System;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Nancy.Owin;
using System.IO;
using System.Net;
//using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.SignalR;

namespace webserver
{
    class Program
    {
        static void Main(string[] args)
        {
            var host = new WebHostBuilder()
                .UseContentRoot(Directory.GetCurrentDirectory())
                .UseKestrel()
                .UseStartup<Startup>()
                .ConfigureKestrel(options =>
                {
                    options.Listen(IPAddress.Loopback, 5000);
                    options.Listen(IPAddress.Any, 80);
                })
                .Build();
                
            host.Run();
        }
    }

    class Startup
    {
        public void Configure(IApplicationBuilder app)
        {
            //app.UseCors("AllowAll");
            app.UseCors(o => o.AllowAnyOrigin());
            //app.UseSignalR(x => x.MapHub<RoomHub>("/signalr"));
            app.UseOwin(x => x.UseNancy());
        }
        public void ConfigureServices(IServiceCollection services)
        {
            services.AddCors(c => c.AddPolicy("AllowOrigin", o => o.AllowAnyOrigin()));
            services.AddSignalR();
        }
    }
}
