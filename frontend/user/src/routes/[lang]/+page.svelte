<script lang="ts">
	import Head from '$lib/components/Head.svelte';
	import { websiteUrl } from '$lib/utilities/constants';
	import logo from '$lib/images/logo.svg';
	import symbol from '$lib/images/symbol.svg';
	import logoWhite from '$lib/images/logo white.svg';
	import type { PageData } from './$types';
	import tony from '$lib/images/tony.jpg';
	import tonyContact from '$lib/images/contact.jpg';
	import { Directions, DesktopPosition } from '$lib/utilities/enums';
	import { onMount } from 'svelte';
	import mdToHtml from '$lib/utilities/markdown';
	import '$lib/styles/markdown.css';
	import { getI18n } from '$lib/i18n';
	import { page } from '$app/state';

	interface Borders {
		n: boolean;
		s: boolean;
		e: boolean;
		w: Boolean;
	}

	interface mainImageData {
		filename: string;
		imageUrl: string;
		altText: string;
		mainImageConfig: {
			description?: string;
			descriptionFontSize: string;
			descriptionFont: string;
			descriptionAlignment: string;
			phoneConfig: {
				overflow?: boolean;
				imageBorders: Borders;
				logoBorders: Borders;
				descriptionPosition?: 'N' | 'S' | 'E' | 'W';
				logoPosition?: 'N' | 'S' | 'E' | 'W';
			};
			desktopConfig: {
				overflow: boolean;
				imagePosition: 'N' | 'S' | 'E' | 'W';
				descriptionPosition: 'N' | 'S' | 'E' | 'W';
				descriptionBorders: Borders;
				logoPosition: 'N' | 'S' | 'E' | 'W';
				descriptionLogoPosition: 'N' | 'S' | 'E' | 'W';
				logoBorders: Borders;
			};
		};
	}

	const { data }: { data: PageData } = $props();
	const mainImages: mainImageData[] = data.mainImages;

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

	const i18n = getI18n();
</script>

<Head
	title="Vector: Interior Design"
	description={$i18n.language === 'es' ? '' : ''}
	url={page.url.toString()}
	alternateEn={`${websiteUrl}/en`}
	alternateEs={`${websiteUrl}/es`}
	ogTitle="Vector: Interior Design"
	ogDescription={$i18n.language === 'es' ? '' : ''}
/>

<svelte:head>
	<title>Vector: Interior Design</title>

	<meta name="description" content={$i18n.language === 'es' ? '' : ''} />

	<link rel="alternate" hreflang="en" href={`${websiteUrl}/en`} />
	<link rel="alternate" hreflang="es" href={`${websiteUrl}/es`} />
</svelte:head>

{#snippet mainImage(imageData: mainImageData)}
	<div
		class="flex size-full gap-20 lg:hidden"
		class:flex-col={imageData.mainImageConfig.phoneConfig.logoPosition === Directions.N}
		class:flex-col-reverse={imageData.mainImageConfig.phoneConfig.logoPosition === Directions.S}
	>
		{#if imageData.mainImageConfig.phoneConfig.logoPosition}
			<div
				class={`border-vector-orange m-auto w-10/12 ${imageData.mainImageConfig.phoneConfig.logoBorders.n ? 'border-t-2 pt-10' : ''} ${imageData.mainImageConfig.phoneConfig.logoBorders.s ? 'border-b-2 pb-10' : ''} ${imageData.mainImageConfig.phoneConfig.logoBorders.e ? 'border-r-2 pr-10' : ''} ${imageData.mainImageConfig.phoneConfig.logoBorders.w ? 'border-l-2 pl-10' : ''}`}
			>
				<img src={symbol} alt="V" class="mx-auto w-20" />
			</div>
		{/if}
		<figure
			class={`flex size-full items-center ${
				imageData.mainImageConfig.phoneConfig.descriptionPosition === Directions.S
					? 'flex-col-reverse'
					: ''
			} ${imageData.mainImageConfig.phoneConfig.descriptionPosition === Directions.N ? 'flex-col' : 'flex-col-reverse'}`}
		>
			{#if imageData.mainImageConfig.phoneConfig.descriptionPosition && imageData.mainImageConfig.description}
				<figcaption class="flex w-10/12 grow flex-col justify-center text-white">
					<div
						class={`text-vector-cream ${imageData.mainImageConfig.descriptionAlignment} markdownDescription my-16`}
						style={`font-family: ${imageData.mainImageConfig.descriptionFont};`}
					>
						{@html mdToHtml(imageData.mainImageConfig.description)}
					</div>
				</figcaption>
			{/if}
			<div
				class={`border-vector-orange mx-auto ${
					!imageData.mainImageConfig.phoneConfig.overflow ? 'w-5/6' : ''
				} ${imageData.mainImageConfig.phoneConfig.imageBorders.e ? 'border-r-2 pr-20' : ''}`}
			>
				{#if imageData.mainImageConfig.phoneConfig.imageBorders.n}
					<div class="bg-vector-orange max-w-83/10 mx-auto mb-20 h-px w-full"></div>
				{/if}
				<img src={imageData.imageUrl} alt={imageData.altText} />
				{#if imageData.mainImageConfig.phoneConfig.imageBorders.s}
					<div class="bg-vector-orange max-w-83/10 mx-auto mt-20 h-px w-full"></div>
				{/if}
			</div>
		</figure>
	</div>

	<figure
		class={`m-auto hidden h-full max-h-full items-center gap-x-20 lg:flex ${
			imageData.mainImageConfig.desktopConfig.imagePosition === DesktopPosition.LEFT &&
			!imageData.mainImageConfig.desktopConfig.overflow
				? 'xl:pl-25'
				: ''
		} ${
			imageData.mainImageConfig.desktopConfig.imagePosition === DesktopPosition.RIGHT &&
			!imageData.mainImageConfig.desktopConfig.overflow
				? 'xl:pr-25'
				: ''
		} ${
			imageData.mainImageConfig.desktopConfig.descriptionPosition == Directions.E ||
			imageData.mainImageConfig.desktopConfig.logoPosition == Directions.E
				? 'flex-row'
				: ''
		} ${
			imageData.mainImageConfig.desktopConfig.descriptionPosition == Directions.W ||
			imageData.mainImageConfig.desktopConfig.logoPosition == Directions.W
				? 'flex-row-reverse'
				: ''
		}`}
		style={`justify-content: ${
			imageData.mainImageConfig.desktopConfig.imagePosition === DesktopPosition.LEFT
				? 'start'
				: imageData.mainImageConfig.desktopConfig.imagePosition === DesktopPosition.RIGHT
					? 'end'
					: 'center'
		};`}
	>
		<img
			src={imageData.imageUrl}
			alt={imageData.altText}
			class={`min-h-64 ${imageData.mainImageConfig.desktopConfig.overflow ? 'h-full' : 'h-2/3'}`}
		/>

		{#if imageData.mainImageConfig.desktopConfig.descriptionPosition || imageData.mainImageConfig.desktopConfig.logoPosition}
			<figcaption
				class={`max-w-1/2 flex h-full flex-col items-center justify-around ${
					imageData.mainImageConfig.desktopConfig.descriptionLogoPosition === Directions.S
						? 'flex-col-reverse'
						: ''
				}`}
			>
				{#if imageData.mainImageConfig.desktopConfig.logoPosition}
					<div class="h-1/2 w-fit">
						<img
							src={symbol}
							alt="V"
							class="border-vector-orange h-full w-fit p-5"
							class:border-t-4={imageData.mainImageConfig.desktopConfig.logoBorders.n}
							class:border-b-4={imageData.mainImageConfig.desktopConfig.logoBorders.s}
							class:border-r-4={imageData.mainImageConfig.desktopConfig.logoBorders.e}
							class:border-l-4={imageData.mainImageConfig.desktopConfig.logoBorders.w}
						/>
					</div>
				{/if}
				{#if imageData.mainImageConfig.desktopConfig.descriptionPosition && imageData.mainImageConfig.description}
					<div
						class={`markdownDescription border-vector-orange text-white ${imageData.mainImageConfig.descriptionAlignment} font-${imageData.mainImageConfig.descriptionFont} text-vector-cream`}
						class:border-t-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.n}
						class:border-b-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.s}
						class:border-r-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.e}
						class:border-l-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.w}
					>
						{@html mdToHtml(imageData.mainImageConfig.description)}
					</div>
				{/if}
			</figcaption>
		{/if}
	</figure>
{/snippet}

{#each mainImages.slice(0, 1) as image (image.filename)}
	<div class="bg-vector-grey flex h-[calc(100vh-5rem)] min-h-72 pr-10">
		{@render mainImage(image)}
		<ul
			class="font-Nexa text-vector-cream relative my-auto flex h-4/5 flex-col items-end gap-y-2 text-right text-[0.6rem] max-xl:pl-10"
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
					{$i18n.t('about')}
				</a>
			</li>
			<li class="w-fit">
				<a href={`${$i18n.language}/proyectos`} class="hover-link">{$i18n.t('projects')}</a>
			</li>
			<li class="w-fit">
				<a href={`${$i18n.language}/esculturas`} class="hover-link">{$i18n.t('sculptures')}</a>
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
					{$i18n.t('contact')}
				</a>
			</li>
		</ul>
	</div>
{/each}

{#each mainImages.slice(1, 2) as image (image.filename)}
	<div class="h-screen min-h-72">
		{@render mainImage(image)}
	</div>
{/each}

{#each mainImages.slice(2, 4) as image (image.filename)}
	<div class="bg-vector-grey h-screen min-h-72">
		{@render mainImage(image)}
	</div>
{/each}

{#each mainImages.slice(4, 5) as image (image.filename)}
	<div class="h-screen min-h-72">
		{@render mainImage(image)}
	</div>
{/each}

<div
	class="bg-vector-grey relative flex min-h-96 items-center lg:h-screen lg:pl-10 xl:pl-20"
	id="about"
>
	<figure class="gap-x-50 flex h-3/4 flex-col items-center justify-start gap-y-10 lg:flex-row">
		<img src={tony} alt="Diseñador" class="h-full" />
		<figcaption>
			<p class="font-Nexa whitespace-pre-line text-sm">
				{$i18n.t('aboutUs')}
			</p>
		</figcaption>
	</figure>
	<img src={logoWhite} alt="Vector: Interior Design" class="absolute bottom-20 right-20 w-20" />
</div>

{#each mainImages.slice(5, 8) as image (image.filename)}
	<div class="h-screen min-h-72">
		{@render mainImage(image)}
	</div>
{/each}

{#each mainImages.slice(8, -1) as image (image.filename)}
	<div class="bg-vector-grey h-screen min-h-72">
		{@render mainImage(image)}
	</div>
{/each}

<div
	class="lg:pl-15 bg-vector-grey flex h-[90vh] min-h-72 flex-col gap-y-10 overflow-hidden lg:flex-row lg:items-center lg:justify-between xl:justify-evenly"
	id="nav"
>
	<img
		src={mainImages.at(-1)!.imageUrl}
		alt={mainImages.at(-1)!.altText}
		class="lg:max-w-2/3 lg:max-h-4/5 max-w-full"
	/>
	<ul class="text-vector-cream relative flex h-4/5 items-center justify-center gap-5 p-5 text-xl">
		<li class="hover-link font-Nexa relative top-10 z-10 h-fit w-fit md:max-lg:top-20">
			<a href={`${$i18n.language}/esculturas/`}>
				{$i18n.t('sculptures')}
			</a>
		</li>
		<div class="flex size-full w-[2px] flex-col items-center overflow-visible" id="pencil">
			<img src={symbol} alt="V" class="min-h-20 min-w-20" />
			<div class="bg-vector-orange relative bottom-0 h-full w-px"></div>
		</div>
		<li
			class="hover-link font-Nexa relative bottom-0 z-10 w-fit after:relative after:top-1 md:max-lg:bottom-0"
		>
			<a href={`/${$i18n.language}/proyectos/`}>
				{$i18n.t('projects')}
			</a>
		</li>
	</ul>
</div>

<footer class="text-vector-cream" id="contact">
	<div class="font-Nexa relative flex items-center justify-center gap-x-5 py-20">
		<p class="border-vector-orange border-r-1 px-5 py-2 text-2xl">{$i18n.t('contact')}</p>
		<a href="mailto:contact@vectorinterior.design" class="py-5">contact@vectorinterior.design</a>
	</div>
	<div class="bg-vector-grey flex h-20 justify-center p-6">
		<img src={logoWhite} alt="vector: Interior Design" />
	</div>
</footer>

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
