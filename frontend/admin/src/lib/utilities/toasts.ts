import { toast, type SvelteToastOptions } from "@zerodevx/svelte-toast";
import { goto } from "$app/navigation";
import { redirect } from "@sveltejs/kit";
import { browser } from "$app/environment";

const toastStyles = {
    "SUCCESS": {
        theme: {
            '--toastBackground': '#01b21f',
            '--toastBarBackground': '#008116'
        }
    },
    "ERROR": {
        theme: {
            '--toastBackground': '#af0000',
            '--toastBarBackground': '#7e0000'
        }
    },
    "WARNING": {
        theme: {
            '--toastColor': "black",
            '--toastBackground': '#ECE81A',
            '--toastBarBackground': '#adb502'
        }
    }
}

export function createToast(msg: string, style: "SUCCESS" | "ERROR" | "WARNING") {
    toast.push(msg, toastStyles[style]);
}

export function redirectWithToast(url: string, msg: string, style: "SUCCESS" | 'ERROR' | 'WARNING') {
    const query = new URLSearchParams({
        toastMsg: msg,
        toastStyle: style
    }).toString();

    const finalURL = `${url}?${query}`;

    if (browser) goto(finalURL);
    else redirect(302, finalURL);
}
