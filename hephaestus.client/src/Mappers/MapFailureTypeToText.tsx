function mapFailureTypeToText(type: number)
{
    switch (type) {
        case 0:
            return 'Low';
        case 1:
            return 'Mild';
        case 2:
            return 'High';
        case 3:
            return 'Critical';
        default:
            return 'Error';
    }
}

export default mapFailureTypeToText;