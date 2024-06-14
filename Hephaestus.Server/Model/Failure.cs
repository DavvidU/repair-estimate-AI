using Hephaestus.Server.Enums;
using System.ComponentModel.DataAnnotations;

namespace Hephaestus.Server.Model
{
    public class Failure
    {
        [Key]
        public int Id { get; set; }
        
        [Required, Editable(false)]
        public FailureType FailureType { get; set; }
        
        [Required, Editable(false)]
        public string Name { get; set; }
        
        [Required, Editable(false)]
        public DateTime Date { get; set; }
        
        [Required]
        public int PotentialPrice { get; set; }
        
        [Required]
        public DateTime PotentialDate { get; set; }
        
        [Required]
        public Status Status { get; set; }
        
        [Required]
        public string RepairDescription { get; set; }
    }
}
