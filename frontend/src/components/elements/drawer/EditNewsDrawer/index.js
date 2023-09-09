import { CardMedia, TextField } from '@mui/material';
import { Stack } from '@mui/system';
import React, { useContext, useState, useEffect } from 'react';
import TagChip from '../../chips/TagChip';
import BaseDrawer from '../BaseDrawer';
import { styled } from '@mui/material/styles';
import AppButton from '../../buttons/AppButton';
import { MainContext } from '../../../../context/MainContextProvider';
import API from '../../../../api';

const TitleInput = styled(TextField)({
  '& input': {
    fontFamily: 'inherit',
    fontWeight: 700,
    fontSize: '20px',
    lineHeight: '22px',
    color: '#25222C',
  },
});

const TextInput = styled(TextField)({
  '& input': {
    fontFamily: 'inherit',
    fontWeight: 400,
    fontSize: '14px',
    lineHeight: '16px',
    color: '#25222C',
  },
});


export default function EditNewsDrawer({ open, onClose }) {
  const { newsSelected, setIsEditDrawerOpen } = useContext(MainContext);
  const [selectedPhoto, setSelectedPhoto] = useState([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (newsSelected) {
      setSelectedPhoto(newsSelected.media[0]);
      setDescription(newsSelected.description);
      setName(newsSelected.name);
      setLoading(false);
    }
  }, [newsSelected]);

  const handleChangeTitle = e => {
    setName(e.target.value);
  };

  const handleChangeText = e => {
    setDescription(e.target.value);
  };

  const handleSelectPhoto = img => {
    setSelectedPhoto(img);
  };

  const handleSubmit = e => {
    e.preventDefault();
    const patchNews = async () => {
      const newsData = {
        "name": name,
        "description": description,
      }
      const result = await API.patch(`/news/${newsSelected.guid}`, newsData, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } });
      console.log(result);
      setIsEditDrawerOpen(false);
    };
    patchNews();
    
  };

  return (
    loading ? null :
      <BaseDrawer open={open} onClose={onClose}>
        <Stack
          component='form'
          onSubmit={handleSubmit}
          sx={{ width: '694px', p: 4, gap: '32px' }}>
          <TitleInput
            value={name}
            onChange={handleChangeTitle}
            placeholder='Заголовок'
            variant='outlined'
          />
          <Stack sx={{ gap: '16px' }}>
            <CardMedia
              component='img'
              height='360'
              image={selectedPhoto.link}
              alt='bus stop'
              sx={{ borderRadius: '12px' }}
            />
            <Stack direction='row' sx={{ gap: '12px' }}>
              {newsSelected.media.map(media => (
                <img
                  onClick={() => handleSelectPhoto(media)}
                  key={media.guid}
                  src={media.link}
                  width={60}
                  height={48}
                  alt='news'
                  style={{
                    borderRadius: '4px',
                    outline: '2px solid transparent',
                    outlineColor:
                      selectedPhoto.guid === media.guid
                        ? 'var(--color-primary)'
                        : 'transparent',
                    cursor: 'pointer',
                  }}
                />
              ))}
            </Stack>
          </Stack>
          <Stack sx={{ gap: '24px' }}>
            <Stack direction='row' sx={{ gap: '8px' }}>
              {newsSelected.categories.map(category => (
                <TagChip key={category.guid} label={category.name} />
              ))}
            </Stack>
            <TextInput
              value={description}
              onChange={handleChangeText}
              placeholder='Текст'
              variant='outlined'
              multiline
              rows={11}>
              {newsSelected.description}
            </TextInput>
          </Stack>
          <AppButton
            type='submit'
            sx={{
              p: '12px 32px',
              width: 'fit-content',
            }}>
            Сохранить
          </AppButton>
        </Stack>
      </BaseDrawer>
  );
}
