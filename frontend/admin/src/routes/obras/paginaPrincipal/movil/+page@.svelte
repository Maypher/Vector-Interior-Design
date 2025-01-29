<script lang="ts">
	import type { PageData } from './$types';
	import logo from '$lib/images/logo.svg';
	import symbol from '$lib/images/symbol.svg';
	import logoWhite from '$lib/images/logo white.svg';
	import tony from '$lib/images/tony.jpg';
	import tonyContact from '$lib/images/contact.jpg';
	import { Directions, TextAlignment, TextFont } from '$lib/utilities/enums';
	import { mdToHTML } from '$lib/utilities/markdown';
	import { PUBLIC_imageURL } from '$env/static/public';
	import '$lib/styles/markdown.css';
	import Movable from '$lib/components/input/Movable.svelte';
	import Borders from '$lib/components/input/Borders.svelte';
	import { isEqual, cloneDeep } from 'lodash-es';
	import { onMount } from 'svelte';
	import getArrayDifference from '$lib/utilities/arrayOrder';
	import { success } from '$lib/utilities/toasts';
	import graphql from '$lib/utilities/api';

	const { data }: { data: PageData } = $props();
	let originalMainPages: any[] = $state($state.snapshot(data.mainPageImages));
	let updatedMainPageImages: any[] = $state($state.snapshot(data.mainPageImages));

	let preview: boolean = $state(false);
	let saveEnabled: boolean = $derived(!isEqual(originalMainPages, updatedMainPageImages));
	let englishDescription: boolean = $state(false);

	async function updatedMainPagePhone() {
		const query = `
			mutation updateMainPageImage($id: Int!, $descriptionEs: String, $descriptionEn: String, 
				$descriptionAlignment: String, $descriptionFont: String, $index: Int, 
				$phoneConfig: MainPageImagePhoneConfigInput) {
				updateMainPageConfig(id: $id, descriptionEs: $descriptionEs, descriptionEn: $descriptionEn, 
				descriptionAlignment: $descriptionAlignment, descriptionFont: $descriptionFont, index: $index, 
				phoneConfig: $phoneConfig) {
					id
					descriptionEs
					descriptionEn
					descriptionFont
					descriptionAlignment
					phoneConfig {
						descriptionPosition
						logoPosition
						imageBorders {
							n
							s
							e
							w
						}
						logoBorders {
							n
							s
							e
							w
						}
						overflow
					}
					image {
						id
						filename
						altText
					}
				}
			}
		`;

		const originalOrder = originalMainPages.map((x) => x.mainImageConfig.id);
		const updatedOrder = updatedMainPageImages.map((x) => x.mainImageConfig.id);
		const ordersToUpdate = getArrayDifference(originalOrder, updatedOrder);
		let updatedValues: any[] = [];

		for (const [i, image] of updatedMainPageImages.entries()) {
			// If there aren't any changes between the original and updated config then don't updated it in the backend.
			if (!isEqual(image, originalMainPages.at(i))) {
				const mainPageConfig = image.mainImageConfig;
				const variables = {
					id: mainPageConfig.id,
					descriptionEs: mainPageConfig.descriptionEs,
					descriptionEn: mainPageConfig.descriptionEn,
					descriptionAlignment: mainPageConfig.descriptionAlignment,
					index: ordersToUpdate.find((val) => val.id === mainPageConfig.id)?.newPos,
					phoneConfig: mainPageConfig.phoneConfig
				};

				const { image: updatedImage, ...updatedData } = (await graphql(query, variables))
					.updateMainPageConfig;

				const resObject = {
					...updatedImage,
					mainImageConfig: {
						...updatedData
					}
				};

				updatedValues.push(resObject);
			} else updatedValues.push(image); // Just add it to the new list to keep the order
		}

		originalMainPages = updatedValues;
		// Doing this way because if it assigns it directly  then both originalMainPage and updatedMainPageImages
		// reference the same object and updates affect both variables.
		updatedMainPageImages = cloneDeep(updatedValues);
		success('Página principal actualizada con éxito.');
	}

	onMount(() => {
		const pencilObserver = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						const pencil = document.getElementById('pencil');
						if (pencil) {
							pencil.id = '';
							pencil.classList.add('pencil-animate');
							pencilObserver.unobserve(entry.target);
						}
					}
				});
			},
			{
				threshold: 0.6
			}
		);

		const pencil = document.getElementById('pencil-wrapper');
		if (pencil) pencilObserver.observe(pencil);
	});
</script>

{#snippet mainImage(imageData: any)}
	<div
		class="flex size-full gap-20 @md:hidden"
		class:flex-col={imageData.mainImageConfig.phoneConfig.logoPosition === Directions.N}
		class:flex-col-reverse={imageData.mainImageConfig.phoneConfig.logoPosition === Directions.S}
	>
		{#if imageData.mainImageConfig.phoneConfig.logoPosition}
			{#if !preview}
				<Movable
					up={imageData.mainImageConfig.phoneConfig.logoPosition !== Directions.N
						? () => (imageData.mainImageConfig.phoneConfig.logoPosition = Directions.N)
						: undefined}
					down={imageData.mainImageConfig.phoneConfig.logoPosition !== Directions.S
						? () => (imageData.mainImageConfig.phoneConfig.logoPosition = Directions.S)
						: undefined}
					class="border-white m-auto w-10/12"
					bind:preview
				>
					<Borders
						id={`logo-${imageData.filename}`}
						bind:n={imageData.mainImageConfig.phoneConfig.logoBorders.n}
						bind:s={imageData.mainImageConfig.phoneConfig.logoBorders.s}
						bind:e={imageData.mainImageConfig.phoneConfig.logoBorders.e}
						bind:w={imageData.mainImageConfig.phoneConfig.logoBorders.w}
					>
						<img src={symbol} alt="symbol" class="mx-auto w-20" />
					</Borders>
				</Movable>
			{:else}
				<div
					class={`border-vector-orange m-auto w-10/12 ${
						imageData.mainImageConfig.phoneConfig.logoBorders.n ? 'border-t-2 pt-10' : ''
					} ${imageData.mainImageConfig.phoneConfig.logoBorders.s ? 'border-b-2 pb-10' : ''} ${
						imageData.mainImageConfig.phoneConfig.logoBorders.e ? 'border-r-2 pr-10' : ''
					} ${imageData.mainImageConfig.phoneConfig.logoBorders.w ? 'border-l-2 pl-10' : ''}`}
				>
					<img src={symbol} alt="symbol" class="mx-auto w-20" />
				</div>
			{/if}
		{/if}
		<div
			class={`flex gap-16 ${
				imageData.mainImageConfig.phoneConfig.descriptionPosition === Directions.S
					? 'flex-col-reverse'
					: ''
			} ${imageData.mainImageConfig.phoneConfig.descriptionPosition === Directions.N ? 'flex-col' : ''}`}
		>
			{#if imageData.mainImageConfig.phoneConfig.descriptionPosition && imageData.mainImageConfig.descriptionEs}
				<Movable
					up={imageData.mainImageConfig.phoneConfig.descriptionPosition !== Directions.N
						? () => (imageData.mainImageConfig.phoneConfig.descriptionPosition = Directions.N)
						: undefined}
					down={imageData.mainImageConfig.phoneConfig.descriptionPosition !== Directions.S
						? () => (imageData.mainImageConfig.phoneConfig.descriptionPosition = Directions.S)
						: undefined}
					class={`class m-auto w-10/12 text-white ${imageData.mainImageConfig.descriptionAlignment} markdownDescription flex flex-col`}
					style={`font-family: ${imageData.mainImageConfig.descriptionFont};`}
					bind:preview
				>
					{#if !preview}
						<div class="flex flex-col justify-between xl:flex-row gap-1">
							<div class="flex flex-col">
								<label for={`main-image-desc-alignment-${imageData.id}`} class="text-white"
									>Alineación</label
								>
								<select
									id={`main-image-desc-alignment-${imageData.id}`}
									bind:value={imageData.mainImageConfig.descriptionAlignment}
									class="bg-white text-black w-fit m-auto"
								>
									{#each Object.entries(TextAlignment) as [key, val] (key)}
										<option value={val}>{key}</option>
									{/each}
								</select>
							</div>
							<div class="flex items-center justify-center">
								<label
									for={`main-image-desc-lang-${imageData.id}`}
									class="hover:cursor-pointer bg-vector-grey p-1 rounded-xs hover:brightness-75 transition-colors select-none text-black"
									>{englishDescription ? 'Inglés' : 'Español'}</label
								>
								<input
									type="checkbox"
									id={`main-image-desc-lang-${imageData.id}`}
									bind:checked={englishDescription}
									hidden
								/>
							</div>
							<div class="flex flex-col">
								<label for={`main-image-desc-font-${imageData.id}`} class="text-white"
									>Tipografía</label
								>
								<select
									id={`main-image-desc-font-${imageData.id}`}
									bind:value={imageData.mainImageConfig.descriptionFont}
									class="bg-white text-black w-fit m-auto"
								>
									{#each Object.entries(TextFont) as [key, val] (key)}
										<option value={val}>{key}</option>
									{/each}
								</select>
							</div>
						</div>
						{#if englishDescription}
							<textarea
								class={`text-white bg-transparent border-2 border-dashed w-full border-white h-full p-5 ${imageData.mainImageConfig.descriptionAlignment} font-${imageData.mainImageConfig.descriptionFont}`}
								bind:value={imageData.mainImageConfig.descriptionEn}
							></textarea>
						{:else}
							<textarea
								class={`text-white bg-transparent border-2 border-dashed w-full border-white h-full p-5 ${imageData.mainImageConfig.descriptionAlignment} font-${imageData.mainImageConfig.descriptionFont}`}
								bind:value={imageData.mainImageConfig.descriptionEs}
							></textarea>
						{/if}
					{:else}
						<div
							class={`markdownDescription text-white ${imageData.mainImageConfig.descriptionAlignment} font-${imageData.mainImageConfig.descriptionFont}`}
						>
							{@html mdToHTML(
								englishDescription
									? imageData.mainImageConfig.descriptionEn
									: imageData.mainImageConfig.descriptionEs
							)}
						</div>
					{/if}
				</Movable>
			{/if}
			{#if !preview}
				<Borders
					id={`image-${imageData.filename}`}
					bind:n={imageData.mainImageConfig.phoneConfig.imageBorders.n}
					bind:s={imageData.mainImageConfig.phoneConfig.imageBorders.s}
					bind:e={imageData.mainImageConfig.phoneConfig.imageBorders.e}
					bind:w={imageData.mainImageConfig.phoneConfig.imageBorders.w}
					class={`relative m-auto transition-all ${!imageData.mainImageConfig.phoneConfig.overflow ? 'w-5/6' : 'w-full'}`}
				>
					<img src={`${PUBLIC_imageURL}${imageData.filename}`} alt={imageData.altText} />
					<div class="absolute top-0 flex justify-between w-full">
						<div>
							<button
								class="text-white hover:bg-gray-200/40 p-2 transition-colors size-10"
								title={imageData.mainImageConfig.phoneConfig.descriptionPosition
									? 'Remover descripción'
									: 'Añadir descripción'}
								onclick={() => {
									if (!imageData.mainImageConfig.phoneConfig.descriptionPosition) {
										imageData.mainImageConfig.phoneConfig.descriptionPosition =
											imageData.mainImageConfig.phoneConfig.logoPosition || Directions.S;
									} else imageData.mainImageConfig.phoneConfig.descriptionPosition = null;
								}}
							>
								<span class="material-symbols-outlined">
									{imageData.mainImageConfig.phoneConfig.descriptionPosition
										? 'delete'
										: 'description'}
								</span>
							</button>
							<button
								title="Logo"
								class="size-10 p-2 hover:bg-gray-200/40"
								onclick={() => {
									if (!imageData.mainImageConfig.phoneConfig.logoPosition) {
										imageData.mainImageConfig.phoneConfig.logoPosition =
											imageData.mainImageConfig.phoneConfig.descriptionPosition || Directions.S;
									} else imageData.mainImageConfig.phoneConfig.logoPosition = null;
								}}
							>
								<img src={symbol} alt="symbol" class="size-full" />
							</button>
						</div>
						<input
							type="checkbox"
							id={`overflow-${imageData.filename}`}
							hidden
							bind:checked={imageData.mainImageConfig.phoneConfig.overflow}
						/>
						<label
							for={`overflow-${imageData.filename}`}
							class="text-white hover:bg-gray-200/40 p-1 flex items-center"
						>
							<span class="material-symbols-outlined">
								{imageData.mainImageConfig.phoneConfig.overflow
									? 'photo_size_select_small'
									: 'photo_size_select_large'}
							</span>
						</label>
					</div>
				</Borders>
			{:else}
				<div
					class={`relative border-vector-orange m-auto transition-all ${!imageData.mainImageConfig.phoneConfig.overflow ? 'w-5/6' : 'w-full'} ${imageData.mainImageConfig.phoneConfig.imageBorders.e ? 'border-r-2 pr-20' : ''} ${imageData.mainImageConfig.phoneConfig.imageBorders.w ? 'border-l-2 pl-20' : ''}`}
				>
					{#if imageData.mainImageConfig.phoneConfig.imageBorders.n}
						<div class="bg-vector-orange max-w-83/10 mx-auto mb-20 h-px w-full"></div>
					{/if}
					<img src={`${PUBLIC_imageURL}${imageData.filename}`} alt={imageData.altText} />
					{#if imageData.mainImageConfig.phoneConfig.imageBorders.s}
						<div class="bg-vector-orange max-w-83/10 mx-auto mt-20 h-px w-full"></div>
					{/if}
				</div>
			{/if}
		</div>
	</div>
{/snippet}

<div class="min-h-screen bg-black flex flex-col items-center">
	<div class="fixed top-5 right-5 flex flex-col items-end gap-2 z-30 opacity-70 hover:opacity-100">
		<input id="previewToggle" type="checkbox" bind:checked={preview} hidden />
		<label
			for="previewToggle"
			title="Vista Previa"
			class="hover:cursor-pointer z-10 bg-gray-200/30 hover:bg-gray-200 rounded-xs"
		>
			<span class="material-symbols-outlined text-4xl select-none">
				{preview ? 'preview_off' : 'preview'}
			</span>
		</label>
		<button
			class="bg-green-500 disabled:brightness-50 hover:brightness-90 p-2 disabled:cursor-not-allowed rounded-xs transition-colors"
			disabled={!saveEnabled}
			onclick={updatedMainPagePhone}>Guardar</button
		>
		<button
			class="bg-red-500 disabled:brightness-50 hover:brightness-90 disabled:cursor-not-allowed p-2 rounded-xs transition-colors"
			disabled={JSON.stringify(originalMainPages) === JSON.stringify(updatedMainPageImages)}
			onclick={() => {
				updatedMainPageImages = $state.snapshot(originalMainPages);
			}}>Cancelar cambios</button
		>
	</div>

	<div class="size-full flex flex-col items-center gap-10">
		<header
			class="bg-vector-grey h-28 p-5 hidden items-center justify-center gap-20 w-full md:flex"
		>
			<a href="/" class="h-full">
				<img src={logo} alt="logo" class="h-full" />
			</a>
			<p class="font-Agency-FB tracking-widest text-4xl text-center" style="word-spacing: 1.5rem;">
				Obras únicas y exclusivas
			</p>
		</header>
		<div
			class="bg-black md:border-2 md:border-white md:aspect-[9/16] w-full md:w-sm flex flex-col overflow-y-scroll overflow-x-clip relative"
		>
			<div
				class="bg-black z-10 h-10 shrink-0 md:border-white md:border-2 w-full hidden md:flex sticky top-0 justify-center items-center"
			>
				<div class="size-4 rounded-xl border-2 border-white hidden md:block"></div>
			</div>
			<div class="size-full @container flex flex-col">
				<header class="bg-vector-grey flex h-28 items-center justify-center gap-20 p-5">
					<a href="/" class="h-full">
						<img src={logo} alt="logo" class="h-full" />
					</a>
					<p
						class="font-Agency-FB hidden w-fit text-center text-4xl tracking-widest @xl:inline"
						style="word-spacing: 1.5rem;"
					>
						Obras únicas y exclusivas
					</p>
				</header>
				<div class="size-full">
					{#each updatedMainPageImages.slice(0, 1) as image, i (image.filename)}
						<Movable
							down={() => {
								const fromIndex = i;
								const element = updatedMainPageImages.splice(fromIndex, 1)[0];
								updatedMainPageImages.splice(fromIndex + 1, 0, element);
							}}
							class={`transition-all mb-20`}
							bind:preview
						>
							{@render mainImage(image)}
						</Movable>
					{/each}
					{#each updatedMainPageImages.slice(1, 5) as image, i (image.filename)}
						<Movable
							up={() => {
								const fromIndex = i + 1; // Adding once since the first image is at the top then it should start at index 1
								const element = updatedMainPageImages.splice(fromIndex, 1)[0];
								updatedMainPageImages.splice(fromIndex - 1, 0, element);
							}}
							down={i + 1 !== updatedMainPageImages.length - 1
								? () => {
										const fromIndex = i + 1;
										const element = updatedMainPageImages.splice(fromIndex, 1)[0];
										updatedMainPageImages.splice(fromIndex + 1, 0, element);
									}
								: undefined}
							bind:preview
							class="my-20"
						>
							{@render mainImage(image)}
						</Movable>
					{/each}
					<div
						class="@lg:my-50 relative my-20 flex flex-col items-center justify-start gap-x-5 gap-y-10 @lg:ml-10 @lg:h-[85vh] @lg:flex-row @xl:ml-20"
					>
						<img src={tony} alt="Diseñador" class="max-h-[70vh]" />
						<div
							class="mx-auto flex h-full w-3/4 flex-col items-center justify-center gap-20 text-justify indent-3 text-lg text-white @lg:w-1/2 @lg:items-end"
						>
							<p>
								{`De lo sublime a lo majestuoso, el límite de este  este diseñador es infinito. Definiendo la personalidad de sus clientes es capaz de convertir los espacios más simples en obras únicas y exclusivas, logrando un impacto visual certero y a veces hasta inimaginable.`}
							</p>
							<img src={logoWhite} alt="Logo white" class="w-44" />
						</div>
					</div>
					{#each updatedMainPageImages.slice(5, 8) as image, i (image.filename)}
						<Movable
							up={() => {
								const fromIndex = i + 6; // Adding once since the first image is at the top then it should start at index 1
								const element = updatedMainPageImages.splice(fromIndex, 1)[0];
								updatedMainPageImages.splice(fromIndex - 1, 0, element);
							}}
							down={i + 6 !== updatedMainPageImages.length - 1
								? () => {
										const fromIndex = i + 6;
										const element = updatedMainPageImages.splice(fromIndex, 1)[0];
										updatedMainPageImages.splice(fromIndex + 1, 0, element);
									}
								: undefined}
							bind:preview
							class="my-20"
						>
							{@render mainImage(image)}
						</Movable>
					{/each}

					<div
						class="border-vector-orange @lg:my-50 m-auto my-20 w-5/6 border-2 p-8 text-center font-[Bahnschrift] text-2xl font-thin tracking-[0.5rem] text-white @md:w-fit @md:text-4xl"
						style="word-spacing: 1rem;"
					>
						Interior Design
					</div>

					{#each updatedMainPageImages.slice(8, -1) as image, i (image.filename)}
						<Movable
							up={() => {
								const fromIndex = i + 8; // Adding once since the first image is at the top then it should start at index 1
								const element = updatedMainPageImages.splice(fromIndex, 1)[0];
								updatedMainPageImages.splice(fromIndex - 1, 0, element);
							}}
							down={i + 8 !== updatedMainPageImages.length - 1
								? () => {
										const fromIndex = i + 8;
										const element = updatedMainPageImages.splice(fromIndex, 1)[0];
										updatedMainPageImages.splice(fromIndex + 1, 0, element);
									}
								: undefined}
							bind:preview
							class="my-20 h-fit"
						>
							{@render mainImage(image)}
						</Movable>
					{/each}

					{#each updatedMainPageImages.slice(-1) as image, i (image.filename)}
						<Movable
							up={() => {
								const fromIndex = i + updatedMainPageImages.length - 1; // Adding once since the first image is at the top then it should start at index 1
								const element = updatedMainPageImages.splice(fromIndex, 1)[0];
								updatedMainPageImages.splice(fromIndex - 1, 0, element);
							}}
							bind:preview
							id="pencil-wrapper"
							class="@lg:my-50 @lg:ml-15 mt-20 flex h-screen flex-col gap-y-10 overflow-visible @lg:h-[70vh] @lg:flex-row @lg:justify-between @xl:h-[90vh] @xl:justify-evenly"
						>
							<img
								src={`${PUBLIC_imageURL}${updatedMainPageImages.at(-1)!.filename}`}
								alt={updatedMainPageImages.at(-1)!.altText}
								class="@lg:max-w-2/3 max-w-full @lg:my-auto @lg:max-h-full"
							/>
							<div class="relative flex size-full items-center justify-center gap-5 p-5">
								<a
									href="/esculturas/"
									class="border-vector-orange after:bg-vector-orange relative top-10 w-fit text-4xl text-white hover:border-b-2 z-20"
									style="font-family: Agency-FB;"
								>
									Esculturas
								</a>
								<div
									class="z-10 flex size-full w-[2px] flex-col items-center overflow-visible"
									id="pencil"
								>
									<img src={symbol} alt="Logo" class="min-h-32 min-w-32" />
									<div class="bg-vector-orange relative bottom-1.5 h-full w-[2px]"></div>
								</div>
								<a
									href="/proyectos/"
									class="border-vector-orange relative bottom-10 w-fit text-4xl text-white hover:border-b-2 z-20"
									style="font-family: Agency-FB;"
									>Proyectos
								</a>
							</div>
						</Movable>
					{/each}
					<footer
						class="my-15 relative flex flex-col items-center justify-center gap-10 @lg:flex-row"
					>
						<div class="max-w-4/5 @lg:max-w-6/7 relative grid gap-y-5">
							<div
								class="flex size-fit flex-col gap-4 self-end justify-self-start text-white"
								style="font-family: Agency-FB; font-size: 5rem; line-height: 4rem;"
							>
								<p>CON</p>
								<p class="indent-[2.1ch]">TAC</p>
								<p
									class="col-start-2 row-start-2 text-center indent-[3.9ch] text-[5rem] text-white"
									style="font-family: Agency-FB; line-height: 4rem;"
								>
									TO
								</p>
							</div>
							<img
								src={tonyContact}
								alt="Contacto"
								class="col-start-2 block max-h-[70vh] align-middle @xl:max-h-[80vh]"
							/>
							<p class="col-start-2 row-start-2 justify-self-center text-white">Vector@gmail.com</p>
						</div>
						<img
							src={logoWhite}
							alt="Logo white"
							class="max-w-42 bottom-0 right-20 w-1/2 @lg:absolute"
						/>
					</footer>
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	#pencil {
		position: relative;
		top: 110%;
	}

	.pencil-animate {
		position: relative;
		animation: pencil-draw 2s ease-in-out forwards;
	}

	@keyframes pencil-draw {
		from {
			top: 110%;
		}

		to {
			top: 0%;
		}
	}
</style>
