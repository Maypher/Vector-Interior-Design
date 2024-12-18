<script lang="ts">
	import { type Obra } from '$lib/utilities/interfaces';
	import { PUBLIC_apiUrl } from '$env/static/public';
	import { onMount } from 'svelte';
	import type internal from 'stream';

	let searchParams = $state({
		name: '',
		page: 1
	});

	// Used to highlight the search string in the results. Not derived because it should only update on search.
	let nameRegex: RegExp = $state(new RegExp(`(${searchParams.name})`, 'gi'));

	let obraPromise: Promise<{ page: number; pageCount: number; obras: Obra[] }> =
		$state(fetchObras());

	async function fetchObras() {
		nameRegex = new RegExp(`(${searchParams.name})`, 'gi');

		const query = `
			query GetObras($page: Int, $name: String) {
				obras(page: $page, name: $name) {
					page
					pageCount
					obras {
						id
						name
						thumbnail {
							filename
							altText
						}
					}
				}
			}	
		`;

		const res = await fetch(PUBLIC_apiUrl, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				query,
				variables: searchParams
			}),
			credentials: 'include'
		});

		if (res.ok) {
			const data = await res.json();
			return data.data.obras;
		}
	}

	function onclick() {
		obraPromise = fetchObras();
	}

	onMount(() => onclick());
</script>

<div class="bg-red-400 min-h-screen p-4">
	<div class="bg-gray-500 p-2 flex justify-between items-center rounded-lg max-w-md m-auto">
		<input type="text" class="bg-transparent outline-none w-full" bind:value={searchParams.name} />
		<button class="material-symbols-outlined border-l-2 border-gray-700 pl-3" {onclick}>
			search
		</button>
	</div>
	<div class="my-4 max-w-md m-auto">
		{#await obraPromise}
			<p>Cargando...</p>
		{:then data}
			{#if data.obras.length == 0}
				{`Ninguna obra con el nombre ${searchParams.name}`}
			{:else}
				<ul class="list-disc">
					{#each data.obras as obra}
						<li>
							<a href={`/obras/${obra.id}`}>
								{@html obra.name.replace(nameRegex, '<b>$1</b>')}
							</a>
							{#if obra.thumbnail}<img
									src={`/images/${obra.thumbnail.filename}`}
									alt={obra.thumbnail.alt_text}
								/>
							{/if}
						</li>
					{/each}
				</ul>
			{/if}
			<div><p>{data.page}/{data.pageCount}</p></div>
		{/await}
		<a href="/obras/crear">Nueva Obra</a>
	</div>
</div>
