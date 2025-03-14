<script lang="ts">
	import type { PageData } from './$types';
	import logo from '$lib/images/logo.svg';
	import symbol from '$lib/images/symbol.svg';
	import tony from '$lib/images/tony.jpg';
	import tonyContact from '$lib/images/contact.jpg';
	import logoWhite from '$lib/images/logo white.svg';
	import { mdToHTML } from '$lib/utilities/markdown';
	import getArrayDifference from '$lib/utilities/arrayOrder';
	import * as enums from '$lib/utilities/enums';
	import Movable from '$lib/components/editor/Movable.svelte';
	import Borders from '$lib/components/editor/Borders.svelte';
	import '$lib/styles/markdown.css';
	import graphql from '$lib/utilities/api';
	import { success } from '$lib/utilities/toasts';
	import { onMount } from 'svelte';
	import { isEqual, cloneDeep } from 'lodash-es';
	import BgColor from '$lib/components/editor/BgColor.svelte';

	const { data }: { data: PageData } = $props();
	let originalMainPages: any[] = $state($state.snapshot(data.mainPageImages));
	let updatedMainPageImages: any[] = $state($state.snapshot(data.mainPageImages));

	let englishDescription: boolean = $state(false);
	let preview: boolean = $state(false);
	let saveEnabled: boolean = $derived(!isEqual(originalMainPages, updatedMainPageImages));

	async function updatedMainPageDesktop() {
		const query = `
			mutation updateMainPageImage($id: Int!, $descriptionEs: String, $descriptionEn: String, 
				$descriptionAlignment: String, $bgColor: String, $descriptionFont: String, $index: Int, 
				$desktopConfig: MainPageImageDesktopConfigInput) {
				updateMainPageConfig(id: $id, descriptionEs: $descriptionEs, descriptionEn: $descriptionEn, 
				descriptionAlignment: $descriptionAlignment, bgColor: $bgColor, descriptionFont: $descriptionFont, index: $index, 
				desktopConfig: $desktopConfig) {
					id
					descriptionEs
					descriptionEn
					descriptionFont
					descriptionAlignment
					bgColor
					desktopConfig {
						imagePosition
						descriptionPosition
						descriptionBorders {
							n
							s
							e
							w
						}
						logoPosition
						logoBorders {
							n
							s
							e
							w
						}
						descriptionLogoPosition
						descriptionLogoBorders {
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
						altTextEs
						imageUrl
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
					descriptionFont: mainPageConfig.descriptionFont,
					descriptionAlignment: mainPageConfig.descriptionAlignment,
					bgColor: mainPageConfig.bgColor,
					index: ordersToUpdate.find((val) => val.id === mainPageConfig.id)?.newPos,
					desktopConfig: mainPageConfig.desktopConfig
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

{#snippet MainImage(image: any)}
	<div
		class={`m-auto size-full items-center flex transition-all ${
			image.mainImageConfig.desktopConfig.imagePosition === enums.DesktopPosition.LEFT &&
			!image.mainImageConfig.desktopConfig.overflow
				? 'xl:pl-20'
				: ''
		} ${
			image.mainImageConfig.desktopConfig.imagePosition === enums.DesktopPosition.RIGHT &&
			!image.mainImageConfig.desktopConfig.overflow
				? 'xl:pr-20'
				: ''
		} ${
			image.mainImageConfig.desktopConfig.descriptionPosition == enums.Directions.E ||
			image.mainImageConfig.desktopConfig.logoPosition == enums.Directions.E
				? 'flex-row'
				: ''
		} ${
			image.mainImageConfig.desktopConfig.descriptionPosition == enums.Directions.W ||
			image.mainImageConfig.desktopConfig.logoPosition == enums.Directions.W
				? 'flex-row-reverse'
				: ''
		}`}
		style={`justify-content: ${
			image.mainImageConfig.desktopConfig.imagePosition === enums.DesktopPosition.LEFT
				? 'start'
				: image.mainImageConfig.desktopConfig.imagePosition === enums.DesktopPosition.RIGHT
					? 'end'
					: 'center'
		}; background-color: ${image.mainImageConfig.bgColor};`}
	>
		<Movable
			left={image.mainImageConfig.desktopConfig.imagePosition !== enums.DesktopPosition.LEFT
				? () => {
						if (
							image.mainImageConfig.desktopConfig.descriptionPosition ||
							image.mainImageConfig.desktopConfig.logoPosition
						) {
							// If there's a description or logo only change between right and left
							image.mainImageConfig.desktopConfig.imagePosition = enums.DesktopPosition.LEFT;
							if (image.mainImageConfig.desktopConfig.descriptionPosition)
								image.mainImageConfig.desktopConfig.descriptionPosition = enums.Directions.E;
							if (image.mainImageConfig.desktopConfig.logoPosition)
								image.mainImageConfig.desktopConfig.logoPosition = enums.Directions.E;
						} else {
							// Otherwise interpolate between left, center, right.
							const enumValues = Object.values(enums.DesktopPosition);
							const currentValue = image.mainImageConfig.desktopConfig.imagePosition;
							const currentIndex = enumValues.indexOf(currentValue);
							image.mainImageConfig.desktopConfig.imagePosition =
								enumValues[currentIndex - 1] || currentValue;
						}
					}
				: undefined}
			right={image.mainImageConfig.desktopConfig.imagePosition !== enums.DesktopPosition.RIGHT
				? () => {
						if (
							image.mainImageConfig.desktopConfig.descriptionPosition ||
							image.mainImageConfig.desktopConfig.logoPosition
						) {
							// If there's a description or logo only change between right and left
							image.mainImageConfig.desktopConfig.imagePosition = enums.DesktopPosition.RIGHT;
							if (image.mainImageConfig.desktopConfig.descriptionPosition)
								image.mainImageConfig.desktopConfig.descriptionPosition = enums.Directions.W;
							if (image.mainImageConfig.desktopConfig.logoPosition)
								image.mainImageConfig.desktopConfig.logoPosition = enums.Directions.W;
						} else {
							const enumValues = Object.values(enums.DesktopPosition);
							const currentValue = image.mainImageConfig.desktopConfig.imagePosition;
							const currentIndex = enumValues.indexOf(currentValue);
							image.mainImageConfig.desktopConfig.imagePosition =
								enumValues[currentIndex + 1] || currentValue;
						}
					}
				: undefined}
			bind:preview
			class={`relative h-full w-fit transition-all`}
		>
			<img src={image.imageUrl} alt={image.altTextEs} class="h-full max-w-full transition-all" />
			<div class="absolute top-0 w-full flex justify-between" class:hidden={preview}>
				<div class="flex rounded-br-sm">
					<button
						class="text-white hover:bg-gray-200/40 p-2 transition-colors size-10"
						title={image.mainImageConfig.desktopConfig.descriptionPosition
							? 'Remover descripción'
							: 'Añadir descripción'}
						onclick={() => {
							if (!image.mainImageConfig.desktopConfig.descriptionPosition) {
								const newPosition =
									image.mainImageConfig.desktopConfig.logoPosition || enums.Directions.E;
								image.mainImageConfig.desktopConfig.descriptionPosition = newPosition;
								image.mainImageConfig.desktopConfig.imagePosition =
									newPosition == enums.Directions.E
										? enums.DesktopPosition.LEFT
										: enums.DesktopPosition.RIGHT;
							} else image.mainImageConfig.desktopConfig.descriptionPosition = null;
						}}
					>
						<span class="material-symbols-outlined">
							{image.mainImageConfig.desktopConfig.descriptionPosition ? 'delete' : 'description'}
						</span>
					</button>
					<button
						title="Logo"
						class="size-10 p-2 hover:bg-gray-200/40"
						onclick={() => {
							if (!image.mainImageConfig.desktopConfig.logoPosition) {
								const newPosition =
									image.mainImageConfig.desktopConfig.descriptionPosition || enums.Directions.E;
								image.mainImageConfig.desktopConfig.logoPosition = newPosition;
								image.mainImageConfig.desktopConfig.descriptionLogoPosition = enums.Directions.N;
								image.mainImageConfig.desktopConfig.imagePosition =
									newPosition == enums.Directions.E
										? enums.DesktopPosition.LEFT
										: enums.DesktopPosition.RIGHT;
							} else {
								image.mainImageConfig.desktopConfig.logoPosition = null;
							}
						}}
					>
						<img src={symbol} alt="symbol" class="size-full" />
					</button>
					<BgColor bind:color={image.mainImageConfig.bgColor} imageId={image.id} />
				</div>
				<button
					class="absolute top-0 right-0 text-white hover:bg-gray-200/40 rounded-bl-sm transition-colors size-10 p-2"
					title="Sangrar"
					onclick={() => {
						image.mainImageConfig.desktopConfig.overflow =
							!image.mainImageConfig.desktopConfig.overflow;
					}}
				>
					<span class="material-symbols-outlined">
						{image.mainImageConfig.desktopConfig.overflow
							? 'photo_size_select_small'
							: 'photo_size_select_large'}
					</span>
				</button>
			</div>
		</Movable>
		{#if image.mainImageConfig.desktopConfig.descriptionPosition || image.mainImageConfig.desktopConfig.logoPosition}
			<div
				class={`flex h-full ${!preview ? 'w-fit' : 'max-w-1/2 m-auto'} grow flex-col items-center justify-around gap-20 ${
					image.mainImageConfig.desktopConfig.descriptionLogoPosition === enums.Directions.S
						? 'flex-col-reverse'
						: ''
				}`}
				class:flex-col-reverse={image.mainImageConfig.desktopConfig.descriptionLogoPosition ===
					enums.Directions.S}
			>
				{#if image.mainImageConfig.desktopConfig.logoPosition}
					{#if !preview}
						<Movable
							up={image.mainImageConfig.desktopConfig.descriptionLogoPosition !==
								enums.Directions.N && image.mainImageConfig.desktopConfig.descriptionPosition
								? () => {
										image.mainImageConfig.desktopConfig.descriptionLogoPosition =
											enums.Directions.N;
									}
								: undefined}
							down={image.mainImageConfig.desktopConfig.descriptionLogoPosition !==
								enums.Directions.S && image.mainImageConfig.desktopConfig.descriptionPosition
								? () => {
										image.mainImageConfig.desktopConfig.descriptionLogoPosition =
											enums.Directions.S;
									}
								: undefined}
							bind:preview
							class="h-24 w-fit"
						>
							<Borders
								class="h-full w-fit relative"
								id={`logo-${image.id}`}
								bind:n={image.mainImageConfig.desktopConfig.logoBorders.n}
								bind:s={image.mainImageConfig.desktopConfig.logoBorders.s}
								bind:e={image.mainImageConfig.desktopConfig.logoBorders.e}
								bind:w={image.mainImageConfig.desktopConfig.logoBorders.w}
							>
								<img src={symbol} alt="symbol" class="h-full w-fit" />
							</Borders>
						</Movable>
					{:else}
						<div class="h-1/2 w-fit">
							<img
								src={symbol}
								alt="symbol"
								class="h-full w-fit border-vector-orange p-5"
								class:border-t-4={image.mainImageConfig.desktopConfig.logoBorders.n}
								class:border-b-4={image.mainImageConfig.desktopConfig.logoBorders.s}
								class:border-r-4={image.mainImageConfig.desktopConfig.logoBorders.e}
								class:border-l-4={image.mainImageConfig.desktopConfig.logoBorders.w}
							/>
						</div>
					{/if}
				{/if}
				{#if image.mainImageConfig.desktopConfig.descriptionPosition}
					{#if !preview}
						<div class="flex items-center justify-center h-full max-h-2/3 w-2/3">
							<Borders
								id={`description-${image.id}`}
								bind:n={image.mainImageConfig.desktopConfig.descriptionBorders.n}
								bind:s={image.mainImageConfig.desktopConfig.descriptionBorders.s}
								bind:e={image.mainImageConfig.desktopConfig.descriptionBorders.e}
								bind:w={image.mainImageConfig.desktopConfig.descriptionBorders.w}
								class="flex flex-col gap-y-5"
							>
								<div class="flex flex-col justify-between xl:flex-row gap-1">
									<div class="flex flex-col">
										<label for={`main-image-desc-alignment-${image.id}`} class="text-white"
											>Alineación</label
										>
										<select
											id={`main-image-desc-alignment-${image.id}`}
											bind:value={image.mainImageConfig.descriptionAlignment}
											class="bg-white"
										>
											{#each Object.entries(enums.TextAlignment) as [key, val] (key)}
												<option value={val}>{key}</option>
											{/each}
										</select>
									</div>
									<div class="flex items-center justify-center">
										<label
											for={`main-image-desc-lang-${image.id}`}
											class="hover:cursor-pointer bg-vector-grey p-1 rounded-xs hover:brightness-75 transition-colors select-none"
											>{englishDescription ? 'Inglés' : 'Español'}</label
										>
										<input
											type="checkbox"
											id={`main-image-desc-lang-${image.id}`}
											bind:checked={englishDescription}
											hidden
										/>
									</div>
									<div class="flex flex-col">
										<label for={`main-image-desc-font-${image.id}`} class="text-white"
											>Tipografía</label
										>
										<select
											id={`main-image-desc-font-${image.id}`}
											bind:value={image.mainImageConfig.descriptionFont}
											class="bg-white"
										>
											{#each Object.entries(enums.TextFont) as [key, val] (key)}
												<option value={val}>{key}</option>
											{/each}
										</select>
									</div>
								</div>
								{#if englishDescription}
									<textarea
										class={`text-white bg-transparent border-2 border-dashed w-full border-white h-full p-5 ${image.mainImageConfig.descriptionAlignment} font-${image.mainImageConfig.descriptionFont}`}
										bind:value={image.mainImageConfig.descriptionEn}
									></textarea>
								{:else}
									<textarea
										class={`text-white bg-transparent border-2 border-dashed w-full border-white h-full p-5 ${image.mainImageConfig.descriptionAlignment} font-${image.mainImageConfig.descriptionFont}`}
										bind:value={image.mainImageConfig.descriptionEs}
									></textarea>
								{/if}
							</Borders>
						</div>
					{:else}
						<div
							class={`markdownDescription text-white border-vector-orange ${image.mainImageConfig.descriptionAlignment} font-${image.mainImageConfig.descriptionFont}`}
							class:border-t-4={image.mainImageConfig.desktopConfig.descriptionBorders.n}
							class:border-b-4={image.mainImageConfig.desktopConfig.descriptionBorders.s}
							class:border-r-4={image.mainImageConfig.desktopConfig.descriptionBorders.e}
							class:border-l-4={image.mainImageConfig.desktopConfig.descriptionBorders.w}
						>
							{@html mdToHTML(
								englishDescription
									? image.mainImageConfig.descriptionEn
									: image.mainImageConfig.descriptionEs
							)}
						</div>
					{/if}
				{/if}
			</div>
		{/if}
	</div>
{/snippet}

<div class="bg-black relative hidden md:block">
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
			onclick={updatedMainPageDesktop}>Guardar</button
		>
		<button
			class="bg-red-500 disabled:brightness-50 hover:brightness-90 disabled:cursor-not-allowed p-2 rounded-xs transition-colors"
			disabled={JSON.stringify(originalMainPages) === JSON.stringify(updatedMainPageImages)}
			onclick={() => {
				updatedMainPageImages = $state.snapshot(originalMainPages);
			}}>Cancelar cambios</button
		>
	</div>
	{#each updatedMainPageImages.slice(0, 1) as image, i (image.filename)}
		<header class="bg-vector-cream h-26 p-5 flex items-center justify-center gap-20">
			<a href="/" class="h-full">
				<img src={logo} alt="logo" class="h-full" />
			</a>
		</header>
		<Movable
			down={() => {
				const fromIndex = i;
				const element = updatedMainPageImages.splice(fromIndex, 1)[0];
				updatedMainPageImages.splice(fromIndex + 1, 0, element);
			}}
			class={`transition-all mb-50 ${image.mainImageConfig.desktopConfig.overflow ? 'header-screen' : 'h-[calc(80vh-7rem)]  mt-20'}`}
			bind:preview
		>
			{@render MainImage(image)}
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
			class={`my-50 transition-all ${!image.mainImageConfig.desktopConfig.overflow ? 'h-[80vh]' : 'h-screen'}`}
		>
			{@render MainImage(image)}
		</Movable>
	{/each}

	<div
		class="lg:my-50 relative my-20 flex flex-col items-center justify-start gap-x-5 gap-y-10 lg:ml-10 lg:h-[85vh] lg:flex-row xl:ml-20"
	>
		<img src={tony} alt="Diseñador" class="max-h-[70vh]" />
		<div
			class="mx-auto flex h-full w-3/4 flex-col items-center justify-center gap-20 text-justify indent-3 text-lg text-white lg:w-1/2 lg:items-end whitespace-pre-line"
		>
			<p>
				{`De lo sublime a lo majestuoso, el límite de este diseñador es infinito. Definiendo la personalidad de sus clientes es capaz de convertir los espacios más simples en obras únicas y exclusivas, logrando un impacto visual certero e inimaginable.`}
			</p>
			<img src={logoWhite} alt="Logo white" class="w-44" />
		</div>
	</div>

	{#each updatedMainPageImages.slice(5, 8) as image, i (image.filename)}
		<Movable
			up={() => {
				const fromIndex = i + 5; // Adding once since the first image is at the top then it should start at index 1
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
			class="my-50 h-[80vh]"
		>
			{@render MainImage(image)}
		</Movable>
	{/each}

	<div
		class="border-vector-orange lg:my-50 m-auto my-20 w-5/6 border-2 p-8 text-center font-[Bahnschrift] text-2xl font-thin tracking-[0.5rem] text-white md:w-fit md:text-4xl"
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
			class="my-50 h-[80vh]"
		>
			{@render MainImage(image)}
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
			class="p-15 lg:my-50 mt-20 flex h-screen flex-col gap-y-10 overflow-visible lg:h-[70vh] lg:flex-row lg:justify-between xl:h-[90vh] xl:justify-evenly"
			style={`background-color: ${image.mainImageConfig.bgColor};`}
		>
			<div class="max-w-2/3 md:max-lg:max-w-full lg:my-auto lg:max-h-full relative">
				<img
					src={updatedMainPageImages.at(-1)!.imageUrl}
					alt={updatedMainPageImages.at(-1)!.altTextEs}
					class="h-full w-auto"
				/>
				<div class="absolute left-0 top-0">
					<BgColor bind:color={image.mainImageConfig.bgColor} imageId={image.filename} />
				</div>
			</div>
			<div class="relative flex size-full items-center justify-center gap-5 p-5">
				<a
					href="/obras/esculturas/"
					class="border-vector-orange after:bg-vector-orange relative top-10 w-fit text-4xl text-white hover:border-b-2 z-20"
					style="font-family: Agency-FB;"
				>
					Esculturas
				</a>
				<div class="z-10 flex size-full w-[2px] flex-col items-center overflow-visible" id="pencil">
					<img src={symbol} alt="Logo" class="min-h-32 min-w-32" />
					<div class="bg-vector-orange relative bottom-4.5 h-full w-[2px]"></div>
				</div>
				<a
					href="/obras/"
					class="border-vector-orange relative bottom-10 w-fit text-4xl text-white hover:border-b-2 z-20"
					style="font-family: Agency-FB;"
					>Proyectos
				</a>
			</div>
		</Movable>
	{/each}

	<footer class="my-15 relative flex flex-col items-center justify-center gap-10 lg:flex-row">
		<div class="max-w-4/5 lg:max-w-6/7 relative grid gap-y-5">
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
				class="col-start-2 block max-h-[70vh] align-middle xl:max-h-[80vh]"
			/>
			<p class="col-start-2 row-start-2 justify-self-center text-white">
				contact@vectorinterior.design
			</p>
		</div>
		<img src={logoWhite} alt="Logo white" class="max-w-42 bottom-0 right-20 w-1/2 lg:absolute" />
	</footer>
</div>

<div class="flex p-10 items-center md:hidden bg-black h-screen">
	<h1 class="text-4xl text-white h-fit text-center border-dashed border-2 border-white p-10">
		Pantalla muy pequeña para mostrar este contenido. Intente rotar el dispositivo.
	</h1>
</div>

<style>
	:global body {
		background-color: black;
	}

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
