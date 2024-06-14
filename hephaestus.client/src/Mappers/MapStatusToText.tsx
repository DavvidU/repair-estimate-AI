function MapStatusToText(status: number)
{
    switch (status) {
        case 0:
            return 'New';
        case 1:
            return 'In Progress';
        case 2:
            return 'Finished';
        case 3:
            return 'Unrepairable';
        default:
            return 'Error';
    }
}

export default MapStatusToText;