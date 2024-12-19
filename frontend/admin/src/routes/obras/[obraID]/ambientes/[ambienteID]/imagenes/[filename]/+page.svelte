<script lang="ts">
	import { yup } from 'sveltekit-superforms/adapters';
	import type { PageData } from './$types';
	import { superForm } from 'sveltekit-superforms';
	import SuperDebug from 'sveltekit-superforms';
	import { imageUpdateSchema } from '$lib/utilities/yupSchemas';
	import EditableInput from '$lib/components/input/EditableInput.svelte';
	import { PUBLIC_apiUrl } from '$env/static/public';
	import { success } from '$lib/utilities/toasts';

	const { data }: { data: PageData } = $props();
	let imageData = $state(data.imageData!);
	let submitting: boolean = $state(false);

	const { form, errors, enhance, constraints } = superForm(data.updateForm!, {
		SPA: true,
		validators: yup(imageUpdateSchema),
		resetForm: false,
		async onUpdate({ form: updateForm }) {
			submitting = true;
			if (updateForm.valid) {
				const query = `
					mutation updateImage($filename: String!, $altText: String!) {
						updateImage(filename: $filename, altText: $altText) {
							altText
						}
					}
				`;

				const variables = { filename: imageData.filename, ...updateForm.data };

				const res = await fetch(PUBLIC_apiUrl, {
					method: 'POST',
					body: JSON.stringify({ query, variables }),
					credentials: 'include',
					headers: {
						'Content-Type': 'application/json'
					}
				});

				if (res.ok) {
					const updatedImageData = (await res.json()).data.updateImage;

					success(`Imagen actualizada con éxito.`);

					$form.altText = updatedImageData.altText;
				}
			}
			submitting = false;
		}
	});
</script>

<div class="w-full bg-green-600">
	<img src={`http://localhost:8080/images/${imageData.filename}`} alt={imageData.altText} />
	<p>{$form.altText}</p>

	<form use:enhance>
		<fieldset disabled={submitting}>
			<EditableInput
				name="name"
				label="Nombre"
				bind:value={$form.altText}
				errors={$errors.altText}
				type="text"
				{...$constraints.altText}
			/>
			<button>Actualizar</button>
		</fieldset>
	</form>
</div>
