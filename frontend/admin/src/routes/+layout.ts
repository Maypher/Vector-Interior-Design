import { createToast } from "$lib/utilities/toasts.js";
import { toast } from "@zerodevx/svelte-toast";

export function load({ url }) {
    toast.pop(0);
    let toastMsg = url.searchParams.get("toastMsg");
    let toastStyle = url.searchParams.get("toastStyle");

    if (toastMsg && toastStyle) {
        createToast(toastMsg, toastStyle as "SUCCESS" | "ERROR" | "WARNING");
    }
}
