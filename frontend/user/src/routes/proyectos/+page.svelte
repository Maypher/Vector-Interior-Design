<script lang="ts">
	import { PUBLIC_imagesUrl } from '$env/static/public';
	import logo from '$lib/images/logo.svg';
	import type { PageData } from './$types';

	const { data }: { data: PageData } = $props();
	const obras = data.obras;
</script>

<header class="bg-vector-grey absolute top-0 z-10 flex justify-center p-5">
	<img src={logo} alt="logo" class="w-[55%]" />
</header>

<div class="h-dvh w-screen snap-y snap-mandatory overflow-y-scroll">
	{#each obras as obra, i (obra.id)}
		{#if obra.thumbnail}
			<div class="flex h-dvh snap-center items-center justify-center bg-black text-white">
				<div class="relative top-16">
					<a href={`/proyectos/${obra.id}`} class="flex flex-col gap-6 px-8">
						<img
							src={`${PUBLIC_imagesUrl}${obra.thumbnail.filename}`}
							alt={obra.thumbnail.altText}
						/>
						<p class="font-Agency-FB text-[1.7rem]">{obra.name}</p>
					</a>
				</div>
			</div>
		{/if}
		{#if i === 0}
			<div id="arrow" inert></div>
		{/if}
	{/each}
</div>

<style>
	#arrow {
		position: absolute;
		bottom: 2%;
		left: 50%;
		transform: translate(-50%, 0) rotate(45deg);
		height: 20px;
		width: 20px;
		border-bottom: 5px solid white;
		border-right: 5px solid white;
		border-radius: 2px;
	}
</style>
