<script lang="ts">
	import { DesktopPosition, Directions } from '$lib/utilities/enums';
	import symbol from '$lib/images/symbol.svg';
	import mdToHtml from '$lib/utilities/markdown';
	import '$lib/styles/skeleton.css';

	const { imageData }: { imageData: any } = $props();
	const hasDescription =
		imageData.mainImageConfig.desktopConfig.descriptionPosition &&
		imageData.mainImageConfig.description;

	let imgLoadedMobile: boolean = $state(false);
	let imgLoadedDesktop: boolean = $state(false);
</script>

{#snippet skeletonText()}
	<div class="flex w-full flex-col items-center justify-center">
		<div class="skeleton skeleton-line"></div>
		<div class="skeleton skeleton-line"></div>
		<div class="skeleton skeleton-line"></div>
		<div class="skeleton skeleton-line"></div>
	</div>
{/snippet}

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
			<figcaption
				class="max-w-5/6 flex w-fit grow flex-col justify-center text-white"
				class:hidden={!imgLoadedMobile}
			>
				<div
					class={`text-vector-cream ${imageData.mainImageConfig.descriptionAlignment} markdownDescription ${
						imageData.mainImageConfig.phoneConfig.descriptionPosition === Directions.N
							? 'mb-16'
							: 'mt-16'
					}`}
					style={`font-family: ${imageData.mainImageConfig.descriptionFont};`}
				>
					{@html mdToHtml(imageData.mainImageConfig.description)}
				</div>
			</figcaption>
			<div class="max-w-5/6 flex grow items-center" class:hidden={imgLoadedMobile}>
				{@render skeletonText()}
			</div>
		{/if}
		<div
			class={`border-vector-orange mx-auto w-full ${
				!imageData.mainImageConfig.phoneConfig.overflow ? 'max-w-5/6' : ''
			} ${imageData.mainImageConfig.phoneConfig.imageBorders.e ? 'border-r-2 pr-20' : ''}`}
		>
			{#if imageData.mainImageConfig.phoneConfig.imageBorders.n}
				<div class="bg-vector-orange max-w-83/10 mx-auto mb-20 h-px w-full"></div>
			{/if}

			<img
				src={imageData.imageUrl}
				alt={imageData.altText}
				class:hidden={!imgLoadedMobile}
				class="min-h-120 mx-auto max-h-[80svh] object-contain"
				onload={() => (imgLoadedMobile = true)}
			/>
			<div class="skeleton aspect-square max-h-[50svh] w-full" class:hidden={imgLoadedMobile}></div>
			{#if imageData.mainImageConfig.phoneConfig.imageBorders.s}
				<div class="bg-vector-orange max-w-83/10 mx-auto mt-20 h-px w-full"></div>
			{/if}
		</div>
	</figure>
</div>

<figure
	class={`m-auto hidden size-full max-h-full items-center gap-x-20 lg:flex ${
		imageData.mainImageConfig.desktopConfig.imagePosition === DesktopPosition.LEFT &&
		!imageData.mainImageConfig.desktopConfig.overflow
			? 'pl-[5%]'
			: ''
	} ${
		imageData.mainImageConfig.desktopConfig.imagePosition === DesktopPosition.RIGHT &&
		!imageData.mainImageConfig.desktopConfig.overflow
			? 'pr-[5%]'
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
		class={`${hasDescription ? 'max-w-1/2 xl:max-w-3/5' : ''} min-h-64 object-contain`}
		class:hidden={!imgLoadedDesktop}
		style={`height: calc(${imageData.mainImageConfig.imageSize} / 100 * 100%);`}
		onload={() => (imgLoadedDesktop = true)}
	/>
	<span
		class="max-w-3/5 bg-vector-black skeleton aspect-square min-h-64"
		class:hidden={imgLoadedDesktop}
		style={`height: calc(${imageData.mainImageConfig.imageSize} / 100 * 100%);`}
	></span>

	{#if imageData.mainImageConfig.desktopConfig.descriptionPosition || imageData.mainImageConfig.desktopConfig.logoPosition}
		<figcaption
			class="max-w-2/5 flex h-full flex-col items-center justify-around"
			class:flex-col-reverse={imageData.mainImageConfig.desktopConfig.descriptionLogoPosition ===
				Directions.S}
			class:hidden={!imgLoadedDesktop}
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
			{#if hasDescription}
				<div
					class={`markdownDescription border-vector-orange ${imageData.mainImageConfig.descriptionAlignment} font-${imageData.mainImageConfig.descriptionFont} text-vector-cream`}
					class:border-t-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.n}
					class:border-b-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.s}
					class:border-r-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.e}
					class:border-l-4={imageData.mainImageConfig.desktopConfig.descriptionBorders.w}
				>
					{@html mdToHtml(imageData.mainImageConfig.description!)}
				</div>
			{/if}
		</figcaption>

		{#if hasDescription}
			<div class="max-w-2/5 w-full" class:hidden={imgLoadedDesktop}>
				{@render skeletonText()}
			</div>
		{/if}
	{/if}
</figure>
