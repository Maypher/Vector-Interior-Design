export interface FormErrors {
    [field: string]: Array<string>,
}

export interface UserData {
    name: string,
    email: string,
    id: number
}

export interface Obra {
    id: number,
    name: string,
    area: number,
    description: string,
    thumbnail?: Image,
    ambientes: Array<Ambiente>,
    public: boolean
}

export interface Ambiente {
    id: number,
    name: string,
    description?: string,
    images: Array<Image>
}

export interface Image {
    alt_text: string,
    filename: string
}
