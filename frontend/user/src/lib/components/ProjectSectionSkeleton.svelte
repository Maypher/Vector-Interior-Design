<script lang="ts">
	const { image }: { image: any } = $props();
	import * as enums from '$lib/utilities/enums';
	import mdToHtml from '$lib/utilities/markdown';
	import symbol from '$lib/images/symbol.svg';
	import '$lib/styles/skeleton.css';

	const hasDescription = image.description && image.desktopConfig.descriptionPosition;
	const descTopOrBottom = [enums.Directions.N, enums.Directions.S].includes(
		image.desktopConfig.descriptionPosition
	);

	let imageLoadedDesktop: boolean = $state(false);
	let imageLoadedMobile: boolean = $state(false);
</script>

{#snippet descriptionContainer(
	description: string,
	alignment: string,
	font: string,
	imgLoaded: boolean = true
)}
	{#if imgLoaded}
		<div
			class={`markdownDescription ${alignment} font-${font} size-full`}
			style="text-wrap: balance; text-wrap: pretty;"
		>
			{@html mdToHtml(description)}
		</div>
	{:else}
		<div class="flex size-full flex-col items-center justify-center">
			<div class="skeleton skeleton-line"></div>
			<div class="skeleton skeleton-line"></div>
			<div class="skeleton skeleton-line"></div>
		</div>
	{/if}
{/snippet}

<!--Mobile view-->
<figure
	class={`border-vector-orange px-8! py-25 gap-12 lg:hidden ${
		image.phoneConfig?.borders?.n && 'pt-30 border-t-2'
	} ${image.phoneConfig?.borders?.s && 'pb-30 border-b-2'} ${
		image.phoneConfig?.borders?.e && 'pr-30 border-r'
	} ${image.phoneConfig?.borders?.w && 'pl-30 border-l'}`}
	class:px-8={image.phoneConfig?.alignment !== enums.Alignment.OVERFLOW}
	class:flex={image.phoneConfig?.descriptionPos}
	class:flex-row={image.phoneConfig?.descriptionPos === enums.Directions.W}
	class:flex-row-reverse={image.phoneConfig?.descriptionPos === enums.Directions.E}
	class:flex-col={image.phoneConfig?.descriptionPos === enums.Directions.N}
	class:flex-col-reverse={image.phoneConfig?.descriptionPos === enums.Directions.S}
	class:hidden={!imageLoadedMobile}
	style={`background-color: ${image.bgColor};`}
>
	{#if image.description && image.phoneConfig.descriptionPos}
		<figcaption class="max-w-8/10 mx-auto w-full">
			{@render descriptionContainer(
				image.description,
				image.phoneConfig.descriptionAlignment,
				image.descriptionFont
			)}
		</figcaption>
	{/if}
	<img
		src={image.imageUrl}
		alt={image.altText}
		class={`${[enums.Alignment.RIGHT, enums.Alignment.LEFT].includes(image.phoneConfig?.alignment) ? 'w-4/5' : ''} max-h-160 object-contain`}
		class:ml-auto={image.phoneConfig?.alignment === enums.Alignment.RIGHT}
		class:mr-auto={image.phoneConfig?.alignment === enums.Alignment.LEFT}
		class:mx-auto={image.phoneConfig?.alignment === enums.Alignment.CENTER}
		onload={() => (imageLoadedMobile = true)}
	/>
</figure>

<!--Mobile skeleton load-->
<div
	class="py-15 gap-12 lg:hidden"
	class:px-8={image.phoneConfig?.alignment !== enums.Alignment.OVERFLOW}
	class:flex={image.phoneConfig?.descriptionPos}
	class:flex-row={image.phoneConfig?.descriptionPos === enums.Directions.W}
	class:flex-row-reverse={image.phoneConfig?.descriptionPos === enums.Directions.E}
	class:flex-col={image.phoneConfig?.descriptionPos === enums.Directions.N}
	class:flex-col-reverse={image.phoneConfig?.descriptionPos === enums.Directions.S}
	class:hidden={imageLoadedMobile}
	style={`background-color: ${image.bgColor};`}
>
	{#if image.description && image.phoneConfig.descriptionPos}
		<div class="max-w-8/10 mx-auto w-full">
			{@render descriptionContainer(
				image.description,
				image.phoneConfig.descriptionAlignment,
				image.descriptionFont,
				imageLoadedMobile
			)}
		</div>
	{/if}
	<div
		class={`${[enums.Alignment.RIGHT, enums.Alignment.LEFT].includes(image.phoneConfig?.alignment) ? 'w-4/5' : 'w-full'} skeleton aspect-square`}
		class:ml-auto={image.phoneConfig?.alignment === enums.Alignment.RIGHT}
		class:mr-auto={image.phoneConfig?.alignment === enums.Alignment.LEFT}
		class:mx-auto={image.phoneConfig?.alignment === enums.Alignment.CENTER}
	></div>
</div>

<!--Desktop view (alongside skeleton load)-->
<div
	class={`mx-auto hidden h-full w-fit items-center justify-center gap-10 lg:flex`}
	class:flex-row={image.desktopConfig.descriptionPosition === enums.Directions.E}
	class:flex-row-reverse={image.desktopConfig.descriptionPosition === enums.Directions.W}
	class:flex-col={image.desktopConfig.descriptionPosition === enums.Directions.S}
	class:flex-col-reverse={image.desktopConfig.descriptionPosition === enums.Directions.N}
>
	<figure
		class={`border-vector-orange relative flex size-full items-center justify-center gap-x-12 ${
			image.desktopConfig.groupAlignment === enums.GroupAlignment.Centro ? 'items-center' : ''
		} ${image.desktopConfig.groupAlignment === enums.GroupAlignment.Arriba ? 'items-start' : ''} ${
			image.desktopConfig.groupAlignment === enums.GroupAlignment.Abajo ? 'items-end' : ''
		} ${image.desktopConfig.imageBorders.n ? 'border-t-2' : ''} ${
			image.desktopConfig.imageBorders.s ? 'border-b-2' : ''
		} ${
			image.desktopConfig.groupAlignment === enums.GroupAlignment.Centro ? 'self-center' : ''
		} ${image.desktopConfig.groupAlignment === enums.GroupAlignment.Arriba ? 'self-start' : ''} ${
			image.desktopConfig.groupAlignment === enums.GroupAlignment.Abajo ? 'self-end' : ''
		}`}
		class:flex-row={image.desktopConfig.descriptionPosition === enums.Directions.E}
		class:flex-row-reverse={image.desktopConfig.descriptionPosition === enums.Directions.W}
		class:flex-col={image.desktopConfig.descriptionPosition === enums.Directions.S}
		class:flex-col-reverse={image.desktopConfig.descriptionPosition === enums.Directions.N}
		class:hidden={!imageLoadedDesktop}
		style={`height: calc(${image.desktopConfig.imageSize}/100 * 100%);`}
	>
		<img
			src={image.imageUrl}
			alt={image.altText}
			class={`border-vector-orange ${hasDescription && !descTopOrBottom ? 'max-w-1/2 xl:max-w-full' : ''} h-full w-auto object-contain ${
				image.desktopConfig.imageBorders.e ? 'border-r-2 px-12' : ''
			} ${image.desktopConfig.imageBorders.w ? 'border-l-2 px-12' : ''} `}
			onload={() => (imageLoadedDesktop = true)}
		/>
		{#if hasDescription}
			<figcaption
				class={`border-vector-orange  ${
					image.desktopConfig.descriptionPosition === enums.Directions.N
						? '-top-5 -translate-y-full'
						: image.desktopConfig.descriptionPosition === enums.Directions.S
							? '-bottom-5 translate-y-full'
							: ''
				} ${
					descTopOrBottom ? 'max-w-8/10 absolute' : 'max-w-2/5'
				} ${image.desktopConfig.descriptionBorders.n ? 'border-t-2 pt-5' : ''} ${
					image.desktopConfig.descriptionBorders.s ? 'border-b-2 pb-5' : ''
				} ${image.desktopConfig.descriptionBorders.e ? 'border-r-2 pr-5' : ''} ${
					image.desktopConfig.descriptionBorders.w ? 'border-l-2 pl-5' : ''
				}`}
			>
				{@render descriptionContainer(
					image.description,
					image.desktopConfig.descriptionAlignment,
					image.descriptionFont
				)}
			</figcaption>
		{/if}
	</figure>
	<div
		class={`relative flex size-full items-center justify-center gap-x-12 ${
			image.desktopConfig.groupAlignment === enums.GroupAlignment.Centro ? 'items-center' : ''
		} ${image.desktopConfig.groupAlignment === enums.GroupAlignment.Arriba ? 'items-start' : ''} ${
			image.desktopConfig.groupAlignment === enums.GroupAlignment.Abajo ? 'items-end' : ''
		} ${
			image.desktopConfig.groupAlignment === enums.GroupAlignment.Centro ? 'self-center' : ''
		} ${image.desktopConfig.groupAlignment === enums.GroupAlignment.Arriba ? 'self-start' : ''} ${
			image.desktopConfig.groupAlignment === enums.GroupAlignment.Abajo ? 'self-end' : ''
		}`}
		class:flex-row={image.desktopConfig.descriptionPosition === enums.Directions.E}
		class:flex-row-reverse={image.desktopConfig.descriptionPosition === enums.Directions.W}
		class:flex-col={image.desktopConfig.descriptionPosition === enums.Directions.S}
		class:flex-col-reverse={image.desktopConfig.descriptionPosition === enums.Directions.N}
		class:hidden={imageLoadedDesktop}
		style={`height: calc(${image.desktopConfig.imageSize}/100 * 100%);`}
	>
		<div class="skeleton aspect-square h-full"></div>
		{#if hasDescription}
			{@render descriptionContainer(
				image.description,
				image.desktopConfig.descriptionAlignment,
				image.descriptionFont,
				imageLoadedDesktop
			)}
		{/if}
	</div>
	{#if image.desktopConfig.logoPosition}
		<div class="flex h-1/2 w-fit items-center">
			<img src={symbol} alt="Símbolo" class="h-full" />
		</div>
	{/if}
</div>
