<script lang="ts">
	import type { PageData } from './$types';
	import logo from '$lib/images/logo.svg';
	import { PUBLIC_imagesUrl } from '$env/static/public';
	import '$lib/styles/markdown.css';
	import mdToHtml from '$lib/utilities/markdown';
	import * as enums from '$lib/utilities/enums';

	const { data }: { data: PageData } = $props();
	const projectData = data.projectData;
</script>

<div class="min-h-screen bg-black">
	<header class="bg-vector-grey sticky top-0 z-10 mb-12 p-5">
		<div class="flex items-center justify-around">
			<a href="/" class="w-1/3">
				<img src={logo} alt="logo" class="w-full" />
			</a>
			<p class="font-Agency-FB tracking-widest" style="word-spacing: 0.2rem;">
				Obras únicas y exclusivas
			</p>
		</div>
	</header>

	{#each projectData.spaces.slice(0, 1) as space (space.id)}
		{#if !space.images.at(0)?.hideInProject}
			<img
				src={`${PUBLIC_imagesUrl}${space.images.at(0)?.filename}`}
				alt={space.images.at(0)?.altText}
				class:px-8={space.images.shift()?.phoneConfig.alignment !== enums.Alignment.OVERFLOW}
			/>

			<div class="mx-8 my-12 text-white">
				<h1 class="font-Agency-FB border-b-vector-orange my-2 border-b-2 pb-2 indent-1 text-3xl">
					{projectData.name}
				</h1>
				<p class="font-Arial text-right text-sm">Área: {projectData.area} metros cuadrados</p>
				<div class="white markdownDescription my-6 text-justify">
					{@html mdToHtml(projectData.description)}
				</div>
			</div>
		{/if}
	{/each}

	<div>
		{#each projectData.spaces.slice(0) as space (space.id)}
			{#each space.images as image (image.filename)}
				{#if !image.hideInProject}
					<div
						class={`border-vector-orange my-12 gap-12 ${image.phoneConfig.borders.n && 'border-t-2 pt-12'} ${image.phoneConfig.borders.s && 'border-b-2 pb-12'} ${image.phoneConfig.borders.e && 'border-r-2 pr-12'} ${image.phoneConfig.borders.w && 'border-l-2 pl-12'}`}
						class:mx-8={image.phoneConfig.alignment !== enums.Alignment.OVERFLOW}
						class:flex={image.phoneConfig.descriptionPos}
						class:flex-row={image.phoneConfig.descriptionPos === enums.Directions.W}
						class:flex-row-reverse={image.phoneConfig.descriptionPos === enums.Directions.E}
						class:flex-col={image.phoneConfig.descriptionPos === enums.Directions.N}
						class:flex-col-reverse={image.phoneConfig.descriptionPos === enums.Directions.S}
					>
						{#if image.description && image.phoneConfig.descriptionPos}
							<div
								class={`markdownDescription font-${image.descriptionFont} ${image.phoneConfig.descriptionAlignment}`}
							>
								{@html mdToHtml(image.description)}
							</div>
						{/if}
						<img
							src={`${PUBLIC_imagesUrl}${image.filename}`}
							alt={image.altText}
							class={`${[enums.Alignment.RIGHT, enums.Alignment.LEFT].includes(image.phoneConfig.alignment) ? 'w-2/3' : ''}`}
							class:ml-auto={image.phoneConfig.alignment === enums.Alignment.RIGHT}
							class:mr-auto={image.phoneConfig.alignment === enums.Alignment.LEFT}
						/>
					</div>
				{/if}
			{/each}
		{/each}
	</div>
</div>
