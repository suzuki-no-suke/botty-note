<script lang="ts">
    import { onMount } from 'svelte';
    import { WIKI_BACK_URL } from '$lib/constants';

    let treeData;

    onMount(async () => {
        const response = await fetch(`${WIKI_BACK_URL}/tree`);
        if (response.ok) {
            treeData = await response.json();
            console.log(treeData);
        } else {
            console.error('Failed to fetch tree data');
        }
    });

    let moveFrom;
    let moveTo;

    let folderResult;

    async function move_folder(from: string, to: string) {
        const response = await fetch(`${WIKI_BACK_URL}/folder/move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                move_from: from,
                move_to: to,
            })
        });
        if (response.ok) {
            folderResult = await response.json();
            console.log(folderResult);
        } else {
            console.error('Failed to move folder');
        }
    }

</script>

<h2>list all folders</h2>

{#if treeData && treeData.all_folders}
    <ul>
        {#each Object.values(treeData.all_folders) as f}
            <li>({f.name} / file: {f.num_files}) - {f.fullpath}</li>
        {/each}
    </ul>
{/if}

<hr/>

<h2>Folder Move</h2>

{#if folderResult}
    <p>{folderResult}</p>
{/if}

<label for="move_from">move from
    <input id="move_from" bind:value={moveFrom} />
</label>

<br/>

<label for="move_to"> move to
    <input id="move_to" bind:value={moveTo} />
</label>

<button on:click={() => move_folder(moveFrom, moveTo)}>execute</button>
