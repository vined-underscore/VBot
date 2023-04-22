from typing import List, Any, AsyncGenerator, Optional
import asyncio
import math


class AsyncPaginator:
    """An asynchronous paginator for a given iterable.

    Parameters
        -----------
        iterable: List[:class:`Any`]
            The iterable to paginate.
            
        page_size: :class:`int`
            The number of items to include in each page.
    """

    def __init__(self, iterable: List[Any], page_size: int = 5) -> None:
        self.iterable: List[Any] = iterable
        self.page_size: int = page_size
        self.num_pages: Optional[int] = None

    async def count(self) -> int:
        """Returns the total number of pages in the iterable.
        Returns
        ---------
        :class:`int`
            The count of pages.
        """
            
        if self.num_pages is None:
            self.num_pages = math.ceil(len(self.iterable) / self.page_size)
        return self.num_pages

    async def get_page(self, page_num: int) -> List[Any]:
        """Returns a list of items for the specified page number.
        
        Returns
        ---------
        List[:class:`Any`]
            The page at the index.
        """
            
        start_index = (page_num - 1) * self.page_size
        end_index = start_index + self.page_size
        page_data = self.iterable[start_index:end_index]
        return page_data

    async def iterate_pages(self) -> AsyncGenerator[List[Any], None]:
        """Iterates over all pages of the iterable asynchronously, yielding a list of items for each page.
        
        Returns
        ---------
        AsyncGenerator[:class:`List[Any]`, None]
            An async generator with all of the pages.
        """
        num_pages = await self.count()
        coros = [self.get_page(page_num) for page_num in range(1, num_pages + 1)]
        for future in asyncio.as_completed(coros):
            page_data = await future
            yield page_data

    async def __aiter__(self) -> AsyncGenerator[List[Any], None]:
        """Allows for intuitive iteration over pages using async for.
        
        Returns
        ---------
        AsyncGenerator[:class:`List[Any]`, None]
            An async generator with all of the pages.
        """
        async for page in self.iterate_pages():
            yield page