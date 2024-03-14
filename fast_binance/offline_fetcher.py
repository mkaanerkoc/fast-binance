
import aiohttp
import asyncio
import io
import pandas as pd
import zipfile

from fast_binance.archieve_files import AbstractFile

from fast_binance.utils import (
    chunked_iterable
)

class OfflineFileFetcher:
    def __init__(self):
        self._worker = 250

    async def fetch_files(self, files:list[AbstractFile]):
        res = []
        async with aiohttp.ClientSession() as session:
            for file_chunk in chunked_iterable(files, self._worker):
                res.extend(await self._fetch_chunk(session, file_chunk))
        return res

    async def _fetch_chunk(self, session, files:list[AbstractFile]):
        tasks = []
        for file in files:
            task = asyncio.ensure_future(self._fetch_file(session, file))
            tasks.append(task)
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def _fetch_file(self, session, file):
        '''
        downloads zip file and extract .csv file and add column information
        returns pandas dataframe
        '''
        print(file.source)
        async with session.get(file.source) as resp:
            assert resp.status == 200
            data = await resp.read()
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                fname = archive.namelist()[0]
                data = pd.read_csv(archive.open(fname), dtype=object, header=None)
                data = file.prepare_df(data)
        return data
    
    def download(self, files):
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(self.fetch_files(files))
        return res
