<script lang="ts">
	import { onMount } from 'svelte';
	import graphql from '$lib/utilities/api';

	let searchParams = $state({
		name: '',
		page: 1
	});

	// Used to highlight the search string in the results. Not derived because it should only update on search.
	let nameRegex: RegExp = $state(new RegExp(`(${searchParams.name})`, 'gi'));

	let obraPromise = $state(fetchObras());

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
		return (await graphql(query, searchParams)).obras;
	}

	const onclick = () => (obraPromise = fetchObras());

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
						<li class="bg-green-300 my-1">
							<a href={`/obras/${obra.id}`} class="block w-full hover:bg-gray-600">
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
		<a href="/obras/crear" class="block bg-green-200 w-fit p-2 m-1 rounded-lg hover:bg-violet-700"
			>Nueva Obra</a
		>
	</div>
</div>
