/**
 * Creates a dialog that can be awaited for a response for task confirmation.
 * @param message The message to show in the dialog
 * @returns A promise resolving to true if the task was confirmed else the task was cancelled.
 */
export default async function confirmationDialog(message: string): Promise<boolean> {
    return new Promise((resolve) => {
        let dialogElement = document.createElement("dialog");

        let messageElement = document.createElement("p");
        messageElement.innerHTML = message;

        let confirmBtn = document.createElement("button");
        confirmBtn.textContent = "Confirmar";
        confirmBtn.type = "button";
        confirmBtn.onclick = () => { resolve(true); dialogElement.remove() }

        let cancelBtn = document.createElement("button");
        cancelBtn.textContent = "Cancelar";
        cancelBtn.type = "button";
        cancelBtn.onclick = () => { resolve(false); dialogElement.remove(); }

        let btnWrapper = document.createElement("div");
        btnWrapper.appendChild(confirmBtn);
        btnWrapper.appendChild(cancelBtn);

        dialogElement.appendChild(messageElement);
        btnWrapper.appendChild(confirmBtn);
        btnWrapper.appendChild(cancelBtn);
        dialogElement.appendChild(btnWrapper);

        document.body.appendChild(dialogElement);
        dialogElement.showModal();
    });
}
