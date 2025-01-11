export interface FormErrors {
    [field: string]: Array<string>,
}

export interface UserData {
    name: string,
    email: string,
    id: number
}

export interface Project {
    id: number,
    name: string,
    area: number,
    description: string,
    thumbnail?: Image,
    ambientes: Array<Space>,
    public: boolean
}

export interface Space {
    id: number,
    name: string,
    description?: string,
    images: Array<Image>
}

export interface Image {
    alt_text: string,
    filename: string
}
