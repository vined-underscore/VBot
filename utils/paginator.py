from typing import List, Any, AsyncGenerator
import asyncio


class AsyncPaginator:
    """An asynchronous paginator for a given iterable.

    Args:
        iterable: The iterable to paginate.
        page_size = 5: The number of items to include in each page.
    """

    def __init__(self, iterable: List[Any], page_size: int = 5) -> None:
        self.iterable = iterable
        self.page_size = page_size
        self.num_pages = None

    async def count(self) -> int:
        """Returns the total number of pages in the iterable.

        Returns:
            The number of pages.
        """
        if self.num_pages is None:
            self.num_pages = (len(self.iterable) + self.page_size - 1) // self.page_size
        return self.num_pages

    async def get_page(self, page_num: int) -> List[Any]:
        """Returns a list of items for the specified page number.

        Args:
            page_num: The page number to retrieve.
            
        Returns:
            A list of items for the specified page.
        """
        start_index = (page_num - 1) * self.page_size
        end_index = start_index + self.page_size
        page_data = self.iterable[start_index:end_index]
        return page_data

    async def iterate_pages(self) -> AsyncGenerator[List[Any], None]:
        """Iterates over all pages of the iterable asynchronously, yielding a list of items for each page.

        Returns:
            An async generator that yields a list of items for each page.
        """
        num_pages = await self.count()
        tasks = [self.get_page(page_num) for page_num in range(1, num_pages + 1)]
        pages = await asyncio.gather(*tasks)
        for page in pages:
            yield page