import { format } from 'date-fns';

function MapDateFormat(dateString: string)
{
    const formattedDate = format(new Date(dateString), 'dd/MM/yyyy');
    return formattedDate;
}
export default MapDateFormat;