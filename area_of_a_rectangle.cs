class Program
    {
        static void Main(string[] args)
        {
            int area, length, width;
            Console.Write("Please write the length of your rectangle: ");
            length = Convert.ToInt32(Console.ReadLine());
            Console.Write("Please write the width of your rectangle: ");
            width = Convert.ToInt32(Console.ReadLine());
            area = length * width;
            Console.WriteLine("The area of rectangle : {0}", area);
            Console.ReadKey();
        }
    }
