/**
 * Transforms an object into FormData to be able to send it to the server.
 * @param obj The object to transform into FormData.
 * @returns The FormData ready to be sent.
 */
export default function objectToFormData(obj: Object): FormData {
    let formData = new FormData();

    Object.entries(obj).forEach(([key, val]) => {
        formData.append(key, val);
    });

    return formData;
}
