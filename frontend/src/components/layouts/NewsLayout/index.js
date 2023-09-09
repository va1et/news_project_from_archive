import { Stack } from '@mui/system';
import React, { useContext, useEffect } from 'react';
import { MainContext } from '../../../context/MainContextProvider';
import TabButton from '../../elements/buttons/TabButton';
import NewsDrawer from '../../elements/drawer/NewsDrawer';
import NewsGroup from '../../modules/groups/NewsGroup';
import API from '../../../api';

export default function NewsLayout() {
  const { isNewsDrawerOpen, setIsNewsDrawerOpen } = useContext(MainContext);
  const [categories, setCategories] = React.useState([]);
  const [news, setNews] = React.useState([]);
  const [realNews, setRealNews] = React.useState([]);
  const [tab, setTab] = React.useState(0);
  const [loading, setLoading] = React.useState(true);

  useEffect(() => {
    const getCategories = async () => {
      const result = await API.get(`/category`, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } });
      result.data.unshift({
        "name": "Все",
        "guid": "f2fad807-b1d5-4744-96be-fb7eba5460e9",
      })
      setCategories(result.data);
    };
    const getNews = async () => {
      const result = await API.get(`/news`, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } });
      setNews(result.data);
      setRealNews(result.data);
      setLoading(false);
    };
    getCategories();
    getNews();
  }, []);

  const handleClick = (event) => {
    const index = parseInt(event.target.id);
    setTab(index);
    if (index === 0) {
      setRealNews(news);
    }
    else {
      const filteredNews = news.filter((item) => {
        return item.categories.some((category) => category.name === event.target.innerText)
      });
      setRealNews(filteredNews);
    }
  };

  return (
    loading ? <div>Loading...</div> :
      <>
        <Stack sx={{ gap: '32px', m: '64px auto', maxWidth: 'var(--max-width)' }}>
          <Stack
            direction='row'
            sx={{
              gap: '32px',
              m: '0 auto',
              maxWidth: '100%',
              overflowX: 'auto',
              pb: 1,

              '::-webkit-scrollbar': {
                display: 'none',
              },
            }}>
            {categories.map((category, index) => (
              <TabButton key={category.guid} id={index} sx={{ flexShrink: 0 }} onClick={handleClick} active={tab === index ? true : false}>
                {category.name}
              </TabButton>
            ))}
          </Stack>
          <NewsGroup news={realNews} />
        </Stack>
        <NewsDrawer open={isNewsDrawerOpen} onClose={() => setIsNewsDrawerOpen(false)} />
      </>
  );
}
