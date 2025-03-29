<script lang="ts">
	import { getI18n } from '$lib/i18n';
	import '$lib/styles/skeleton.css';

	interface Props {
		id: number;
		imageUrl: string;
		imageAltText: string;
		projectName: string;
	}

	const { id, imageUrl, imageAltText, projectName }: Props = $props();

	let imgLoadedDesktop: boolean = $state(false);
	let imgLoadedMobile: boolean = $state(false);
	const i18n = getI18n();
</script>

{#snippet projectBlock(imgLoaded: boolean)}
	<div class:hidden={imgLoaded} class="h-full">
		<div class="skeleton h-full" style="aspect-ratio: 9/16;"></div>
		<div class="skeleton skeleton-line"></div>
	</div>
{/snippet}

<!--Mobile view-->
<div class="flex h-full flex-col justify-center lg:hidden">
	<a
		href={`/${$i18n.language}/proyectos/${id}`}
		class="flex h-3/4 flex-col justify-center gap-6 px-8"
	>
		<figure class="h-full" class:hidden={!imgLoadedMobile}>
			<img
				src={imageUrl}
				alt={imageAltText}
				class="h-full object-cover"
				onload={() => (imgLoadedMobile = true)}
			/>
			<figcaption class="my-2">
				<p class="font-Nexa">{projectName}</p>
			</figcaption>
		</figure>
		{@render projectBlock(imgLoadedMobile)}
	</a>
</div>

<!--Desktop view-->
<a
	href={`/${$i18n.language}/proyectos/${id}`}
	class="m-auto hidden h-2/3 w-fit flex-col items-start gap-y-2 transition-transform hover:scale-110 hover:cursor-pointer lg:flex"
>
	<figure class="size-full" class:hidden={!imgLoadedDesktop}>
		<img
			src={imageUrl}
			alt={imageAltText}
			class="h-full"
			onload={() => {
				imgLoadedDesktop = true;
			}}
		/>
		<figcaption>
			<p class="font-Nexa my-5 text-xs font-extralight" style="letter-spacing: 0.1rem;">
				{projectName}
			</p>
		</figcaption>
	</figure>
	{@render projectBlock(imgLoadedDesktop)}
</a>
