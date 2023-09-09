import { CardMedia, Typography } from '@mui/material';
import { Stack } from '@mui/system';
import React, { useEffect, useState, useContext } from 'react';
import TagChip from '../../chips/TagChip';
import BaseDrawer from '../BaseDrawer';
import { styled } from '@mui/material/styles';
import CommentCard from '../../cards/CommentCard';
import { MainContext } from '../../../../context/MainContextProvider';

const Title = styled(Typography)({
  maxWidth: '440px',
  fontFamily: 'inherit',
  fontWeight: 700,
  fontSize: '20px',
  lineHeight: '22px',
  color: '#25222C',
});

const Text = styled(Typography)({
  fontFamily: 'inherit',
  fontWeight: 400,
  fontSize: '14px',
  lineHeight: '16px',
  color: '#25222C',
});


export default function NewsDrawer({ open, onClose }) {
  const { newsSelected } = useContext(MainContext);
  const [selectedPhoto, setSelectedPhoto] = useState();
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    if (newsSelected) {
      setSelectedPhoto(newsSelected.media[0]);
      setLoading(false);
    }
  }, [newsSelected]);

  const handleSelectPhoto = media => {
    setSelectedPhoto(media);
  };

  return (
    newsSelected === null ? null :
      <BaseDrawer open={open} onClose={onClose}>
        <Stack sx={{ width: '684px', p: 4, gap: '32px' }}>
          <Title component='h2'>{newsSelected.name}</Title>
          {loading ? null :
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
          }
          <Stack sx={{ gap: '24px' }}>
            <Stack direction='row' sx={{ gap: '8px' }}>
              {newsSelected.categories.map(category => (
                <TagChip key={category.guid} label={category.name} />
              ))}
            </Stack>
            <Text>{newsSelected.description}</Text>
          </Stack>
          <Stack sx={{ gap: '32px' }}>
            <Title component='h2'>Комментарии</Title>
            <Stack sx={{ gap: '24px' }}>
              {newsSelected.comments.map(comment => (
                <CommentCard key={comment.id} comment={comment} />
              ))}
            </Stack>
          </Stack>
        </Stack>
      </BaseDrawer>
  );
}
