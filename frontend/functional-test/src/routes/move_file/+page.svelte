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

    let folderDetail;

    async function folder_detail(path: string) {
        const response = await fetch(`${WIKI_BACK_URL}/folder/detail?dirpath=${path}`);
        if (response.ok) {
            folderDetail = await response.json();
            console.log(folderDetail);
        } else {
            console.error('Failed to fetch folder detail data');
        }
    };

    let moveFrom;
    let moveTo;

    let fileResult;

    async function move_file(from: string, to: string) {
        const response = await fetch(`${WIKI_BACK_URL}/file/move`, {
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
            fileResult = await response.json();
            console.log(fileResult);
        } else {
            console.error('Failed to move file');
        }
    }

</script>

<h2>list all folders</h2>

{#if treeData && treeData.all_folders}
    <ul>
        {#each Object.values(treeData.all_folders) as f}
            <li><button on:click={() => folder_detail(f.fullpath)} >({f.name} / file: {f.num_files}) - {f.fullpath}</button></li>
        {/each}
    </ul>
{/if}

<hr/>


<h2>Folder Detail</h2>

{#if folderDetail}
<h2>here</h2>
<p>{folderDetail.fullpath}</p>

<h3>parents</h3>
<ul>
    {#each folderDetail.parents as p}
        <li>{p}</li>
    {/each}
</ul>

<h3>files</h3>
<ul>
    {#each folderDetail.files as f}
        <li>{f}</li>
    {/each}
</ul>

<h3>folders</h3>
<ul>
    {#each folderDetail.children as c}
        <li>{c}</li>
    {/each}
</ul>
{/if}

<hr/>

<h2>File Move</h2>

{#if fileResult}
    <p>{fileResult}</p>
{/if}

<label for="move_from">move from
    <input id="move_from" bind:value={moveFrom} />
</label>

<br/>

<label for="move_to"> move to
    <input id="move_to" bind:value={moveTo} />
</label>

<button on:click={() => move_file(moveFrom, moveTo)}>execute</button>
