<script lang="ts">
	import type { PageData } from './$types';
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
				$descriptionAlignment: String, $bgColor: String, $descriptionFont: String, $imageSize: Int, $index: Int, 
				$desktopConfig: MainPageImageDesktopConfigInput) {
				updateMainPageConfig(id: $id, descriptionEs: $descriptionEs, descriptionEn: $descriptionEn, 
				descriptionAlignment: $descriptionAlignment, bgColor: $bgColor, descriptionFont: $descriptionFont, imageSize: $imageSize, index: $index, 
				desktopConfig: $desktopConfig) {
					id
					descriptionEs
					descriptionEn
					descriptionFont
					descriptionAlignment
					bgColor
					imageSize
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
					imageSize: mainPageConfig.imageSize,
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

		const pencil = document.getElementById('nav');
		if (pencil) pencilObserver.observe(pencil);
	});

	function scrollToTop() {
		window.scrollTo({ top: 0, behavior: 'smooth' });
	}
</script>

{#snippet MainImage(image: any)}
	{@const hasDescription: boolean = image.mainImageConfig.desktopConfig.descriptionPosition != null}
	<div class="size-full max-h-full" style={`background-color: ${image.mainImageConfig.bgColor};`}>
		<figure
			class={`mx-auto hidden size-full max-h-full items-center gap-x-20 lg:flex ${
				image.mainImageConfig.desktopConfig.imagePosition === enums.DesktopPosition.LEFT &&
				!image.mainImageConfig.desktopConfig.overflow
					? 'pl-[5%]'
					: ''
			} ${
				image.mainImageConfig.desktopConfig.imagePosition === enums.DesktopPosition.RIGHT &&
				!image.mainImageConfig.desktopConfig.overflow
					? 'pr-[5%]'
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
			};`}
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
				class={`${hasDescription || !preview ? 'max-w-3/5' : ''} ${preview ? 'w-auto' : ''} flex items-center min-h-64 justify-center`}
				style={`${preview ? `height: calc(${image.mainImageConfig.imageSize}/100 * 100%)` : '100%'}`}
			>
				<img
					src={image.imageUrl}
					alt={image.altTextEs}
					class={`${!hasDescription && !preview ? 'object-cover' : 'object-contain'}`}
					style={`height: ${!preview ? `calc(${image.mainImageConfig.imageSize}/100 * 100%)` : '100%'}`}
				/>
				<div
					class="absolute top-0 w-full flex justify-between bg-vector-cream/40"
					class:hidden={preview}
				>
					<div class="flex gap-2 rounded-br-sm">
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
						<div class="bg-vector-cream/40 h-fit p-1 flex items-center">
							<label for={`${image.id}-size`}>Tamaño</label>
							<input
								type="range"
								min="0"
								max="100"
								step="10"
								bind:value={image.mainImageConfig.imageSize}
							/>
							(<input
								type="number"
								min="0"
								max="100"
								step="10"
								bind:value={image.mainImageConfig.imageSize}
							/>)
						</div>
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
				<figcaption
					class={`${preview ? 'max-w-2/5' : 'w-1/2'} flex h-full flex-col items-center justify-around`}
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
												class="hover:cursor-pointer bg-vector-cream p-1 rounded-xs hover:brightness-75 transition-colors select-none"
											>
												{englishDescription ? 'Inglés' : 'Español'}
											</label>
											<input
												type="checkbox"
												id={`main-image-desc-lang-${image.id}`}
												bind:checked={englishDescription}
												hidden
											/>
										</div>
										<div class="flex flex-col">
											<label for={`main-image-desc-font-${image.id}`} class="text-white">
												Tipografía
											</label>
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
								class={`markdownDescription border-vector-orange ${image.mainImageConfig.descriptionAlignment} font-${image.mainImageConfig.descriptionFont}`}
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
				</figcaption>
			{/if}
		</figure>
	</div>
{/snippet}

<div class="bg-vector-black relative hidden md:block">
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
			onclick={updatedMainPageDesktop}
		>
			Guardar
		</button>
		<button
			class="bg-red-500 disabled:brightness-50 hover:brightness-90 disabled:cursor-not-allowed p-2 rounded-xs transition-colors"
			disabled={JSON.stringify(originalMainPages) === JSON.stringify(updatedMainPageImages)}
			onclick={() => {
				updatedMainPageImages = $state.snapshot(originalMainPages);
			}}
		>
			Cancelar cambios
		</button>
	</div>
	<div
		class="header-screen w-full [&_.markdownDescription]:mb-0! min-h-130 flex max-lg:mb-20 xl:pr-10 transition-colors"
		style={`background-color: ${updatedMainPageImages.at(0).mainImageConfig.bgColor};`}
	>
		{#each updatedMainPageImages.slice(0, 1) as image (image.filename)}
			{@render MainImage(image)}
		{/each}
		<ul
			class="font-Nexa text-vector-cream relative my-auto hidden h-4/5 flex-col items-end gap-y-2 text-right text-[0.7em] max-xl:pl-10 xl:flex"
			style="letter-spacing: 0.05rem;"
		>
			<li class="before:bg-vector-orange w-fit">
				<a
					href="#about"
					class="hover-link"
					onclick={(e) => {
						e.preventDefault();

						document
							.getElementById('about')
							?.scrollIntoView({ behavior: 'smooth', block: 'center' });
					}}
				>
					Nosotros
				</a>
			</li>
			<li class="w-fit">
				<a href="/obras" class="hover-link">Proyectos</a>
			</li>
			<li class="w-fit">
				<a href="/obras/esculturas" class="hover-link">Esculturas</a>
			</li>
			<li class="w-fit">
				<a
					href="#contact"
					class="hover-link"
					onclick={(e) => {
						e.preventDefault();

						document
							.getElementById('contact')
							?.scrollIntoView({ behavior: 'smooth', block: 'center' });
					}}
				>
					Contacto
				</a>
			</li>
		</ul>
	</div>
	{#each updatedMainPageImages.slice(1, 5) as image (image.filename)}
		<div
			class="min-h-72 h-svh w-full transition-colors"
			style={`background-color: ${image.mainImageConfig.bgColor};`}
		>
			{@render MainImage(image)}
		</div>
	{/each}

	<div
		class="min-h-120 relative flex items-center pb-40 pt-20 lg:h-screen lg:py-0 lg:pl-0"
		id="about"
	>
		<figure
			class="mx-auto flex flex-col items-center justify-center gap-x-20 gap-y-10 lg:size-full lg:flex-row"
		>
			<img src={tony} alt="Diseñador" class="lg:h-9/10 min-h-92 max-h-[70svh] w-auto" />
			<figcaption class="max-w-1/2">
				<p class="font-Nexa text-vector-cream whitespace-pre-line text-sm">
					<span class="text-4xl brightness-100 [&_br]:hidden [&_em]:not-italic">
						{@html mdToHTML(`Como diseñador 
                de *interiores*,`)}
					</span>
					<span class="mt-5 block brightness-50">
						{`mi enfoque es profundamente personal. No sigo un solo estilo, sino que fusiono influencias de distintas partes del mundo con las últimas tendencias para crear espacios únicos.

                    Mi trabajo se basa en tres pilares fundamentales: confort, funcionalidad y distinción.

                    Cada proyecto es una oportunidad para transformar ideas en ambientes que combinan estética y propósito, siempre con una atención minuciosa a los detalles. 
                    
                    Me involucro en cada etapa del proceso, porque el diseño es mi pasión y creo que la excelencia está en los detalles bien ejecutados.

                    Más que imponer un estilo, interpreto y traduzco las necesidades y aspiraciones de mis clientes en espacios que cuentan su historia. Mi trayectoria y mis proyectos hablan por si solos, respaldados por un compromiso absoluto de calidad con creatividad.`}
					</span>
				</p>
			</figcaption>
		</figure>
		<button
			class="text-vector-cream w-25 lg:bottom-1/10 lg:right-1/20 hover:scale-120 absolute bottom-10 right-1/2 cursor-pointer transition-transform max-lg:translate-x-1/2"
			onclick={scrollToTop}
		>
			<img src={logoWhite} alt="Vector: Interior Design" class="w-full" />
		</button>
	</div>

	{#each updatedMainPageImages.slice(5, -1) as image, i (image.filename)}
		<div
			class="min-h-72 h-svh w-full transition-colors"
			style={`background-color: ${image.mainImageConfig.bgColor};`}
		>
			{@render MainImage(image)}
		</div>
	{/each}

	{#each updatedMainPageImages.slice(-1) as image (image.filename)}
		<div
			class="pt-30 min-h-120 flex flex-col gap-y-10 overflow-hidden lg:h-[70svh] lg:flex-row lg:items-center lg:justify-evenly lg:pt-0 transition-colors"
			id="nav"
			style={`background-color: ${image.mainImageConfig.bgColor};`}
		>
			<div
				class={`lg:max-w-2/3 flex items-center justify-center max-h-full max-w-full relative ${!preview ? 'border-2 w-full' : 'w-auto'} border-dashed border-gray-500`}
				style={`height: ${preview ? `calc(${image.mainImageConfig.imageSize} / 100 * 100%);` : '100%'}`}
			>
				<img
					src={image.imageUrl}
					alt={image.altTextEs}
					class="object-cover"
					style={`height: ${!preview ? `calc(${image.mainImageConfig.imageSize} / 100 * 100%)` : '100%'}`}
				/>
				{#if !preview}
					<div class="absolute left-0 top-0 max-w-1/2">
						<BgColor bind:color={image.mainImageConfig.bgColor} imageId={image.filename} />
					</div>
					<div class="absolute top-0 right-0">
						<div class="bg-vector-cream/40 h-fit p-1 flex items-center">
							<label for={`${image.id}-size`}>Tamaño</label>
							<input
								type="range"
								min="0"
								max="100"
								step="10"
								bind:value={image.mainImageConfig.imageSize}
							/>
							(<input
								type="number"
								min="0"
								max="100"
								step="10"
								bind:value={image.mainImageConfig.imageSize}
							/>)
						</div>
					</div>
				{/if}
			</div>
			<ul
				class="text-vector-cream relative flex items-center justify-center gap-5 p-5 text-xl lg:h-4/5"
			>
				<li class="hover-link font-Nexa relative top-0 z-10 h-fit w-fit">
					<a href="obras/esculturas/" class="text-vector-cream"> Esculturas </a>
				</li>
				<div class="h-92 flex w-[2px] flex-col items-center overflow-visible" id="pencil">
					<img src={symbol} alt="V" class="min-h-20 min-w-20" />
					<div class="bg-vector-orange relative bottom-3 h-2/3 w-px"></div>
				</div>
				<li class="hover-link font-Nexa relative bottom-10 z-10 w-fit after:relative after:top-1">
					<a href="/obras/proyectos/" class="text-vector-cream"> Proyectos </a>
				</li>
			</ul>
		</div>
	{/each}

	<footer class="text-vector-cream" id="contact">
		<div class="font-Nexa relative flex items-center justify-center gap-x-5 py-20">
			<p class="border-vector-orange border-r-1 px-5 py-2 text-2xl">Contacto</p>
			<a href="mailto:contact@vectorinterior.design" class="py-5">contact@vectorinterior.design</a>
		</div>
		<div class="bg-vector-grey flex h-24 justify-center p-6">
			<button
				onclick={scrollToTop}
				class="hover:scale-120 h-full cursor-pointer transition-transform"
			>
				<img src={logoWhite} alt="vector: Interior Design" class="h-full" />
			</button>
		</div>
	</footer>
</div>

<div class="flex p-10 items-center md:hidden bg-black h-screen">
	<h1 class="text-4xl text-white h-fit text-center border-dashed border-2 border-white p-10">
		Pantalla muy pequeña para mostrar este contenido. Intente rotar el dispositivo.
	</h1>
</div>

<style>
	.hover-link::after {
		display: block;
		content: '';
		background-color: var(--color-vector-orange);
		height: 0.13rem;
		width: 100%;
		transition: all 0.3s ease-out;
		transform-origin: right;
		border-radius: 5px;
		transform: scale(0, 1);
		border-radius: 50%;
	}

	.hover-link:hover::after {
		transform: scale(1, 1);
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
			top: 100%;
		}

		to {
			top: 0%;
		}
	}
</style>
