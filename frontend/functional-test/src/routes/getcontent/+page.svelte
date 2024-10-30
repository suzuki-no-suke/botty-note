<script lang="ts">
    import { onMount } from 'svelte';

    let treeData;

    onMount(async () => {
        const response = await fetch('http://localhost:8000/tree');
        if (response.ok) {
            treeData = await response.json();
            console.log(treeData);
        } else {
            console.error('Failed to fetch tree data');
        }
    });

    let folderDetail;

    async function folder_detail(path: string) {
        const response = await fetch(`http://localhost:8000/folder/detail?dirpath=${path}`);
        if (response.ok) {
            folderDetail = await response.json();
            console.log(folderDetail);
        } else {
            console.error('Failed to fetch folder detail data');
        }
    };

    let fileDetail;

    async function get_content(path: string) {
        const response = await fetch(`http://localhost:8000/file/detail?filepath=${path}`);
        if (response.ok) {
            fileDetail = await response.json();
            console.log(fileDetail);
        } else {
            console.error('Failed to fetch file detail data');
        }
    }
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
<p>{folderDetail.fullpath}</p>

<h3>files</h3>
<ul>
    {#each folderDetail.files as f}
        <li><button on:click={() => get_content(folderDetail.fullpath + f)}>{f}</button></li>
    {/each}
</ul>

{:else}
<h3>wait for ready... dir</h3>
{/if}


{#if fileDetail}
<h3>{fileDetail.name} ({fileDetail.fullpath})</h3>

<pre><code>{fileDetail.contents}</code></pre>

{:else}
<h3>wait for ready ... file</h3>
{/if}
