using Hephaestus.Server.Enums;
using Hephaestus.Server.Model;
using Microsoft.EntityFrameworkCore;

namespace Hephaestus.Server.Data
{
    public class HephaestusDbContext : DbContext
    {
        public DbSet<Failure> Failures { get; set; }

        public HephaestusDbContext(DbContextOptions<HephaestusDbContext> options) : base(options) 
        { 
            
        }

        // Fluent API
        protected override void OnModelCreating(ModelBuilder modelBuilder) 
        {
            base.OnModelCreating(modelBuilder);

            /* Typy wyliczeniowe tlumaczone do string przed zapisem do bazy danych */
            
            modelBuilder.Entity<Failure>().Property(e => e.FailureType)
                .HasConversion(v => v.ToString(), v => (FailureType)Enum.Parse(typeof(FailureType), v));

            modelBuilder.Entity<Failure>().Property(e => e.Status)
                .HasConversion(v => v.ToString(), v => (Status)Enum.Parse(typeof(Status), v));
        }
    }
}
