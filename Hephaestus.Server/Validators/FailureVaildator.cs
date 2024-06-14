using Hephaestus.Server.Enums;
using Hephaestus.Server.Model;
using Microsoft.IdentityModel.Tokens;

namespace Hephaestus.Server.Validators
{
    public static class FailureVaildator
    {
        public static bool IsFailureVaild(Failure failure)
        {
            if (!IsFailureTypeValid(failure.FailureType)) return false;
            if (!IsNameValid(failure.Name)) return false;
            if (!IsDateValid(failure.Date)) return false;
            if (!IsPotentialPriceValid(failure.PotentialPrice)) return false;
            if (!IsPotentialDateValid(failure.PotentialDate, failure.Date)) return false;
            if (!IsStatusValid(failure.Status)) return false;
            if (!IsRepairDescriptionValid(failure.RepairDescription)) return false;
            
            return true;
        }
        private static bool IsFailureTypeValid(FailureType failureType) 
        {
            if (failureType == FailureType.Low || failureType == FailureType.Mild ||
                failureType == FailureType.High || failureType == FailureType.Critical)
                return true;
            else
                return false;
        }
        private static bool IsNameValid(string name) 
        {
            if (name.IsNullOrEmpty()) return false;
            else return true;
        }
        private static bool IsDateValid(DateTime date)
        {
            if (date.CompareTo(DateTime.Now.AddHours(8)) > 0) return false;
            else return true;
        }
        private static bool IsPotentialPriceValid(int potentialPrice)
        {
            if (potentialPrice < 0) return false;
            else return true;
        }
        private static bool IsPotentialDateValid(DateTime potentialDate, DateTime date)
        {
            if (potentialDate.CompareTo(date) <= 0) return false;
            else return true;
        }
        private static bool IsStatusValid(Status status)
        {
            if (status == Status.New || status == Status.InProgress ||
                status == Status.Finished || status == Status.Unrepairable)
                return true;
            else
                return false;
        }
        private static bool IsRepairDescriptionValid(string repairDescription)
        {
            if (repairDescription.IsNullOrEmpty()) return false;
            else return true;
        }
    }
}
