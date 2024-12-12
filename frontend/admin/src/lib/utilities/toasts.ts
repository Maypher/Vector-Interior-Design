import { toast } from "@zerodevx/svelte-toast";

export const success = (m: string) => toast.push(m, {
    theme: {
        '--toastBackground': 'green',
        '--toastColor': 'white',
        '--toastBarBackground': 'olive'
    }
})

export const error = (m: string) => toast.push(m, {
    theme: {
        '--toastBackground': 'red',
        '--toastColor': 'white',
        '--toastBarBackground': 'maroon'
    }
})

