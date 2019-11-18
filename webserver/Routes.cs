namespace webserver
{
    using Nancy;
    using System.IO;
    using System;
    using System.Collections.Generic;
    using Newtonsoft.Json;
    using Nancy.Extensions;
    
    public class Routes : NancyModule 
    {
        public static string lastImage = "";
        public static List<Dictionary<string, int>> commands = new List<Dictionary<string, int>>();
        public string GetStringBody()
        {
            var body = this.Request.Body; 
            int length = (int) body.Length;
            byte[] data = new byte[length]; 
            body.Read(data, 0, length);
            return System.Text.Encoding.Default.GetString(data); 
        }
        public Routes()
        {
            Get("/", x =>{ return View["index.html"];});

            Get("/image", x =>{ 
                return lastImage;
                //return Convert.ToBase64String(File.ReadAllBytes("mewtwo.jpg"));
            });

            Get("/command", x =>{
                string response = JsonConvert.SerializeObject(commands);
                commands.Clear();
                return response;
            });

            Post("/command", x=>{
                try{
                    string result = GetStringBody();       
                    commands.Add(JsonConvert.DeserializeObject<Dictionary<string, int>>(result));
                    System.Console.WriteLine();
                }
                catch(Exception e){
                    System.Console.WriteLine(e);
                }
                return 200;
            });

            Post("/image", x =>{
                lastImage = GetStringBody();
                string response = JsonConvert.SerializeObject(commands);
                commands.Clear();
                return response;
            });
        }
    }
}