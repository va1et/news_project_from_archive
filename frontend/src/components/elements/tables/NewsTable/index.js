import React, { useState, useEffect, useContext } from 'react';
import PropTypes from 'prop-types';
import { alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TablePagination from '@mui/material/TablePagination';
import TableRow from '@mui/material/TableRow';
import TableSortLabel from '@mui/material/TableSortLabel';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Checkbox from '@mui/material/Checkbox';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import { visuallyHidden } from '@mui/utils';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import DeleteIcon from '@mui/icons-material/Delete';
import OptionsMenu from '../../menus/OptionsMenu';
import { getComparator, stableSort } from '../../../../utils/functions';
import {
  Button,
  FormControl,
  InputAdornment,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from '@mui/material';
import { Stack } from '@mui/system';
import SearchIcon from '@mui/icons-material/Search';
import Chip from '@mui/material/Chip';
import API from '../../../../api';
import { MainContext } from '../../../../context/MainContextProvider';

const headCells = [
  {
    id: 'date',
    numeric: false,
    disablePadding: true,
    label: 'Дата создания',
  },
  {
    id: 'title',
    numeric: false,
    disablePadding: false,
    label: 'Заголовок',
  },
  {
    id: 'text',
    numeric: false,
    disablePadding: false,
    label: 'Описание',
  },
  {
    id: 'tags',
    numeric: false,
    disablePadding: false,
    label: 'Теги',
  },
  {
    id: 'attachments',
    numeric: false,
    disablePadding: false,
    label: 'Вложения',
  },
  {
    id: 'comments',
    numeric: false,
    disablePadding: false,
    label: 'Комментарии',
  },
  {
    id: 'likes',
    numeric: false,
    disablePadding: false,
    label: 'Оценили',
  },
  {
    id: 'options',
    numeric: false,
    disablePadding: true,
    label: '',
  },
];

function EnhancedTableHead(props) {
  const {
    onSelectAllClick,
    order,
    orderBy,
    numSelected,
    rowCount,
    onRequestSort,
  } = props;
  const createSortHandler = property => event => {
    onRequestSort(event, property);
  };

  return (
    <TableHead>
      <TableRow>
        <TableCell padding='checkbox'>
          <Checkbox
            color='primary'
            indeterminate={numSelected > 0 && numSelected < rowCount}
            checked={rowCount > 0 && numSelected === rowCount}
            onChange={onSelectAllClick}
            inputProps={{
              'aria-label': 'select all desserts',
            }}
          />
        </TableCell>
        {headCells.map(headCell => (
          <TableCell
            key={headCell.id}
            align={'left'}
            padding={headCell.disablePadding ? 'none' : 'normal'}
            sortDirection={orderBy === headCell.id ? order : false}>
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : 'asc'}
              onClick={createSortHandler(headCell.id)}>
              {headCell.label}
              {orderBy === headCell.id ? (
                <Box component='span' sx={visuallyHidden}>
                  {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
                </Box>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}

EnhancedTableHead.propTypes = {
  numSelected: PropTypes.number.isRequired,
  onRequestSort: PropTypes.func.isRequired,
  onSelectAllClick: PropTypes.func.isRequired,
  order: PropTypes.oneOf(['asc', 'desc']).isRequired,
  orderBy: PropTypes.string.isRequired,
  rowCount: PropTypes.number.isRequired,
};

function EnhancedTableToolbar(props) {
  const { numSelected } = props;

  return (
    <>
      {numSelected > 0 ? (
        <Toolbar
          sx={{
            pl: { sm: 2 },
            pr: { xs: 1, sm: 1 },
            ...{
              bgcolor: theme =>
                alpha(
                  theme.palette.primary.main,
                  theme.palette.action.activatedOpacity
                ),
            },
          }}>
          <Typography
            sx={{ flex: '1 1 100%' }}
            color='inherit'
            variant='subtitle1'
            component='div'>
            {numSelected} выбрано
          </Typography>

          <Tooltip title='Delete'>
            <IconButton>
              <DeleteIcon />
            </IconButton>
          </Tooltip>
        </Toolbar>
      ) : null}
    </>
  );
}

EnhancedTableToolbar.propTypes = {
  numSelected: PropTypes.number.isRequired,
};

export default function NewsTable({ rows }) {
  const [order, setOrder] = useState('asc');
  const [orderBy, setOrderBy] = useState('subject');
  const [selected, setSelected] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  const [anchorEl, setAnchorEl] = useState(null);
  const openOptionsMenu = Boolean(anchorEl);
  const [category, setCategory] = useState('');
  const [categories, setCategories] = useState([]);
  const { setNewsSelected } = useContext(MainContext);

  useEffect(() => {
    const getCategories = async () => {
      const result = await API.get(`/category`, { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } });
      setCategories(result.data);
    };
    getCategories();
  }, []);

  const handleChangeCategory = event => {
    setCategory(event.target.value);
  };

  const handleCloseOptionsMenu = () => {
    setAnchorEl(null);
  };

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const handleSelectAllClick = event => {
    if (event.target.checked) {
      const newSelected = rows.map(n => n.date);
      setSelected(newSelected);
      return;
    }
    setSelected([]);
  };

  const handleClick = (event, date) => {
    const selectedIndex = selected.indexOf(date);
    let newSelected = [];

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, date);
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1));
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1));
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1)
      );
    }

    setSelected(newSelected);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = event => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const isSelected = date => selected.indexOf(date) !== -1;

  // Avoid a layout jump when reaching the last page with empty rows.
  const emptyRows =
    page > 0 ? Math.max(0, (1 + page) * rowsPerPage - rows.length) : 0;

  return (
    <>
      <Box sx={{ width: '100%' }}>
        <Paper
          sx={{
            width: '100%',
            mb: 2,
            borderRadius: '12px',
            boxShadow: '0px 4px 20px rgba(83, 83, 83, 0.1)',
          }}>
          <Stack
            direction='row'
            sx={{
              p: '16px',
              gap: '16px',
              alignItems: 'center',
              display: 'grid',
              gridTemplateColumns: '180px 1fr',
            }}>
            <FormControl>
              <InputLabel>Категория</InputLabel>
              <Select
                id='demo-simple-select'
                value={category}
                label='Категория'
                onChange={handleChangeCategory}>
                {categories.map(category => (
                  <MenuItem value={category.guid}>{category.name}</MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              label='Поиск'
              InputProps={{
                startAdornment: (
                  <InputAdornment position='start'>
                    <SearchIcon />
                  </InputAdornment>
                ),
              }}
              variant='outlined'
            />
          </Stack>
          <EnhancedTableToolbar numSelected={selected.length} />
          <TableContainer>
            <Table sx={{ minWidth: 750 }} aria-labelledby='tableTitle'>
              <EnhancedTableHead
                numSelected={selected.length}
                order={order}
                orderBy={orderBy}
                onSelectAllClick={handleSelectAllClick}
                onRequestSort={handleRequestSort}
                rowCount={rows.length}
              />
              <TableBody>
                {/* if you don't need to support IE11, you can replace the `stableSort` call with:
                 rows.sort(getComparator(order, orderBy)).slice() */}
                {stableSort(rows, getComparator(order, orderBy))
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((row, index) => {
                    const isItemSelected = isSelected(row.guid);
                    const labelId = `enhanced-table-checkbox-${index}`;

                    return (
                      <TableRow
                        hover
                        onClick={event => handleClick(event, row.guid)}
                        role='checkbox'
                        aria-checked={isItemSelected}
                        tabIndex={-1}
                        key={row.guid}
                        selected={isItemSelected}>
                        <TableCell padding='checkbox'>
                          <Checkbox
                            color='primary'
                            checked={isItemSelected}
                            inputProps={{
                              'aria-labelledby': labelId,
                            }}
                          />
                        </TableCell>
                        <TableCell
                          component='th'
                          id={labelId}
                          scope='row'
                          padding='none'>
                          {row.created_at.split('T')[0]}
                        </TableCell>
                        <TableCell
                          sx={{
                            maxWidth: '150px',
                            textOverflow: 'ellipsis',
                            overflow: 'hidden',
                            whiteSpace: 'nowrap',
                          }}>
                          {row.name}
                        </TableCell>
                        <TableCell
                          sx={{
                            maxWidth: '200px',
                            textOverflow: 'ellipsis',
                            overflow: 'hidden',
                            whiteSpace: 'nowrap',
                          }}>
                          {row.description}
                        </TableCell>
                        <TableCell>
                          <div
                            style={{
                              maxWidth: '200px',
                              display: 'flex',
                              flexWrap: 'wrap',
                              gap: '8px',
                            }}>
                            {row.categories.map(category => (
                              <Chip key={category.guid} label={category.name} />
                            ))}
                          </div>
                        </TableCell>
                        <TableCell>
                          <Button
                            onClick={e => e.stopPropagation()}
                            href={row.results}
                            download
                            sx={{
                              textTransform: 'none',
                              color: 'var(--color-primary)',
                            }}>
                            {row.media.length} фото
                          </Button>
                        </TableCell>
                        <TableCell>{row.comments.length} комментариев</TableCell>
                        <TableCell>{row.likes} человек</TableCell>
                        <TableCell>
                          <IconButton
                            onClick={e => {
                              e.stopPropagation();
                              setNewsSelected(row);
                              setAnchorEl(e.currentTarget);
                            }}>
                            <MoreVertIcon />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    );
                  })}
                {emptyRows > 0 && (
                  <TableRow
                    style={{
                      height: 53 * emptyRows,
                    }}>
                    <TableCell colSpan={6} />
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component='div'
            count={rows.length}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handleChangePage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Paper>
      </Box>
      <OptionsMenu
        anchorEl={anchorEl}
        open={openOptionsMenu}
        handleClose={handleCloseOptionsMenu}
      />
    </>
  );
}
