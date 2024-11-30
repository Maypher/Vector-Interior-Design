export interface FormErrors {
    [field: string]: Array<string>,
}

export interface UserData {
    name: string,
    email: string,
    id: number
}

export interface ObraData {
    id: number,
    name: string,
    description: string,
    images: Array<{
        filename: string,
        alt_text: string,
        indice: number
    }>
}
