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
</script>

<h2>list all folders</h2>

{#if treeData && treeData.all_folders}
    <ul>
        {#each Object.values(treeData.all_folders) as f}
            <li><button on:click={() => folder_detail(f.fullpath)}>({f.name} / file: {f.num_files}) - {f.fullpath}</button></li>
        {/each}
    </ul>
{/if}

<hr/>

<h2>Folder Detail</h2>

{#if folderDetail}
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


<h3>info</h3>
<table>
    <thead>
        <tr>
            <th>item</th>
            <th>value</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>name</td>
            <td>{folderDetail.name}</td>
        </tr>
        <tr>
            <td>fullpath</td>
            <td>{folderDetail.fullpath}</td>
        </tr>
    </tbody>
</table>

{:else}
<h3>wait for ready...</h3>
{/if}


