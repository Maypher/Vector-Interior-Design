/**
 * Creates a dialog that can be awaited for a response for task confirmation.
 * @param message The message to show in the dialog
 * @returns A promise resolving to true if the task was confirmed else the task was cancelled.
 */
export default async function confirmationDialog(message: string): Promise<boolean> {
    return new Promise((resolve) => {
        let dialogElement = document.createElement("dialog");
        dialogElement.className = "confirmationDialog";

        let wrapper = document.createElement("div");
        wrapper.className = "wrapper";

        let messageElement = document.createElement("p");
        messageElement.innerHTML = message;

        let confirmBtn = document.createElement("button");
        confirmBtn.className = "confirm";
        confirmBtn.textContent = "Confirmar";
        confirmBtn.type = "button";
        confirmBtn.onclick = () => { resolve(true); dialogElement.remove() }

        let cancelBtn = document.createElement("button");
        cancelBtn.className = "cancel";
        cancelBtn.textContent = "Cancelar";
        cancelBtn.type = "button";
        cancelBtn.onclick = () => { resolve(false); dialogElement.remove(); }

        let btnWrapper = document.createElement("div");
        btnWrapper.className = "btnWrapper";

        btnWrapper.appendChild(confirmBtn);
        btnWrapper.appendChild(cancelBtn);

        btnWrapper.appendChild(confirmBtn);
        btnWrapper.appendChild(cancelBtn);

        wrapper.appendChild(messageElement);
        wrapper.appendChild(btnWrapper);

        dialogElement.appendChild(wrapper);

        document.body.appendChild(dialogElement);
        dialogElement.showModal();
    });
}
