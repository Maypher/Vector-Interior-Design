<script lang="ts">
	import { setError, superForm } from 'sveltekit-superforms';
	import type { PageData } from './$types';
	import { yup } from 'sveltekit-superforms/adapters';
	import { imageUpdateSchema } from '$lib/utilities/yupSchemas';
	import TextInput from '$lib/components/input/TextInput.svelte';
	import { PUBLIC_apiUrl } from '$env/static/public';
	import { error } from '$lib/utilities/toasts';
	import { goto } from '$app/navigation';
	import Errors from '$lib/components/input/Errors.svelte';

	const { data }: { data: PageData } = $props();
	let inputFile: FileList | undefined | null = $state();
	let fileErrors: Array<string> = $state([]);
	let submitting: boolean = $state(false);

	const { form, errors, enhance, constraints } = superForm(data.createForm, {
		SPA: true,
		validators: yup(imageUpdateSchema),
		async onUpdate({ form: createForm }) {
			fileErrors = [];
			submitting = true;

			if (createForm.valid) {
				const file = inputFile?.item(0);
				if (!file) {
					fileErrors.push('Imagen requerida.');
					submitting = false;
					return;
				}

				const query = `
                    mutation createImage(
                        $ambienteId: Int!,
                        $file: Upload!,
                        $altText: String!
                        ) {
                        createImage(
                            ambienteId: $ambienteId,
                            image: $file,
                            altText: $altText
                        ) {
                            __typename
                            ... on Image {
                                filename
                            }
                            ... on AmbienteNotFoundImage {
                                ambienteId
                            }
                            ... on UnsupportedFileType {
                                filetype 
                            }
                        }
                        }
                `;

				const variables = {
					file: null,
					altText: createForm.data.altText,
					ambienteId: data.ambienteID
				};

				const operations = JSON.stringify({ query, variables });
				const map = JSON.stringify({ file: ['variables.file'] });

				let formData = new FormData();

				formData.append('operations', operations);
				formData.append('map', map);
				formData.append('file', file);

				const res = await fetch(PUBLIC_apiUrl, {
					method: 'POST',
					body: formData,
					credentials: 'include'
				});

				if (res.ok) {
					const imageData = (await res.json()).data.createImage;

					switch (imageData.__typename) {
						case 'AmbienteNotFoundImage':
							error(
								`No se puede registrar la imagen en ambiente con ID ${imageData.ambienteId} porque no existe.`
							);
							break;
						case 'UnsupportedFileType':
							fileErrors.push(`Archivo tipo ${imageData.fileType} no es válido.`);
							break;
						case 'Image':
							await goto(`/obras/${data.ambienteID}/ambientes/${data.ambienteID}/`);
							break;
					}
				}
			}

			submitting = false;
		}
	});
</script>

<div class="m-5">
	<form use:enhance class="bg-amber-600 max-w-xl m-auto p-3">
		<fieldset disabled={submitting}>
			<input type="file" accept="image/png, image/jpeg" bind:files={inputFile} />
			<Errors errors={fileErrors} />
			<TextInput
				name="altText"
				label="Texto Alternativo"
				type="text"
				bind:value={$form.altText}
				errors={$errors.altText}
				{...$constraints}
			/>
			<button class="bg-green-200 hover:bg-amber-200 p-2 rounded-md">Crear</button>
		</fieldset>
	</form>
</div>
