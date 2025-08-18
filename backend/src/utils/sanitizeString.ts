export const sanitizeString = (input: string): string => {
    const pattern = /[^a-zA-Z0-9\s]/g;
    
    const sanitizedString = input.replace(pattern, '');
    
    const sanitizedStringLower = sanitizedString.toLowerCase();

    return sanitizedStringLower;
}
