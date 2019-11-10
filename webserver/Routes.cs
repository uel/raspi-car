namespace webserver
{
    using Nancy;
    using System.IO;
    using System;
    public class Routes : NancyModule 
    {
        public Routes()
        {
            Get("/", x =>{ return View["index.html"];});

            Get("/image", x =>{ 
                return Convert.ToBase64String(File.ReadAllBytes("mewtwo.jpg"));
            });
        }
    }
}