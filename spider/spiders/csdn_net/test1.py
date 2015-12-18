package com.ufida.report.anareport.expand;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

import nc.pub.smart.metadata.Field;

import com.ufida.report.anareport.IFldCountType;
import com.ufida.report.anareport.data.AbsRowData;
import com.ufida.report.anareport.data.DetailRowData;
import com.ufida.report.anareport.data.GroupDataSet;
import com.ufida.report.anareport.data.GroupRowData;
import com.ufida.report.anareport.data.MemoryRowData;
import com.ufida.report.anareport.data.RowDataArray;
import com.ufida.report.anareport.data.RowDataComparator;
import com.ufida.report.anareport.model.AnaDataSetTool;
import com.ufida.report.anareport.model.AnaRepField;
import com.ufida.report.anareport.model.AreaDataModel;
import com.ufida.report.anareport.model.ElseField;
import com.ufida.report.anareport.model.FieldCountDef;
import com.ufida.report.anareport.model.TopNSetInfo;
import com.ufida.report.anareport.util.FreeFieldConverter;
import com.ufida.report.anareport.util.SortArrayUtil;

public class ListTopNProcessor extends AbsGroupDataProcessor {
	private ArrayList<Integer> al_procLvl = null;

	public ListTopNProcessor(AreaDataModel areaModel) {
		super(areaModel);
		al_procLvl = new ArrayList<Integer>();
	}

	@Override
	protected boolean isEnabledProc(AnaRepField fld) {
		TopNSetInfo topN = (TopNSetInfo) fld.getTopNInfo();
		if (topN != null && topN.isEnabled()) {
			FieldCountDef def = fld.getFieldCountDef();
			if (def != null && !def.hasRangeField())// 对于最外围的“合计”，无法处理TopN
				return false;
			int procLvl = getProcLvl(fld);
			if (al_procLvl.contains(procLvl)) {// 同一个级次上只能有一个生效
				topN.setEnabled(false);
				return false;
			} else {
				al_procLvl.add(procLvl);
				return true;
			}
		}
		return false;
	}

	@Override
	protected ProcRowDatas processRowDatas(GroupDataSet grpDataSet, AbsRowData parentRow, RowDataArray rowData,
			AnaRepField fld, int[] lvlCount, int plvl, String col) {
		TopNSetInfo topN = (TopNSetInfo) fld.getTopNInfo();

		// 进行排序		
		RowDataComparator comp = new RowDataComparator(grpDataSet, col, topN.isASC());
		List<AbsRowData> sortedRows = new ArrayList<AbsRowData>();
		if(rowData == null){
			return null ;
		}
		int len = rowData.length();
		for(int i = 0;i<len;i++){
			sortedRows.add(rowData.get(i));
		}
		SortArrayUtil.sortList(sortedRows, comp);
		
		//int[] idx = SortArrayUtil.sortArrayData(rowData, new RowDataComparator(grpDataSet, col, topN.isASC()));
		int idxLen = (sortedRows == null) ? 0 : sortedRows.size();//(idx == null) ? 0 : idx.length;
		int datalen = topN.isExtendN() ? topN.getN() : Math.min(topN.getN(), idxLen);// 保留的数据行数
		datalen = Math.max(0, datalen);// 确保不是负数

		int retLen = (topN.isShowElse() && (datalen < idxLen || topN.isExtendN())) ? datalen + 1 : datalen;// 存在其他数据或者要强行占位时，都要增加一行
		// 设置返回数据行
		RowDataArray rows = new RowDataArray(retLen);
		for (int i = 0; i < datalen; i++) {
			AbsRowData data = null;
			if (i < idxLen)
				data = sortedRows.get(i);
			else
				data = createNullRow(grpDataSet, idxLen == 0 ? parentRow : rowData.get(0), plvl - 1);
			rows.setRowData(i, data);
		}
		// “其他”
		if (retLen > datalen) {
			AbsRowData data = null;
			if (idxLen > datalen)
				data = getElseRow(grpDataSet, parentRow, rowData, sortedRows, datalen, fld);
			else
				data = createNullElseRow(grpDataSet, idxLen == 0 ? parentRow : rowData.get(0), fld);
			rows.setRowData(datalen, data);
		}
		RowDataArray rmvRows = null;
		if (datalen < idxLen) {// 有舍弃掉的数据
			rmvRows = new RowDataArray(idxLen - datalen);
			for (int i = datalen; i < idxLen; i++) {
				rmvRows.setRowData(i - datalen, sortedRows.get(i));
			}
		}

		ProcRowDatas result = new ProcRowDatas(rows, rmvRows);
		return result;
	}

	/**
	 * edit by guogang 2009-3-3 支持TopN其他字段的各种设置,更复杂的处理???
	 * 
	 * @i18n miufo00335=其他
	 */
	private AbsRowData getElseRow(GroupDataSet grpDataSet, AbsRowData parentRow, RowDataArray rowData,List<AbsRowData> sortedRows,
			int begin, AnaRepField fld) {
		AbsRowData first = rowData.get(0);
		TopNSetInfo topN = (TopNSetInfo) fld.getTopNInfo();

		if (first.isDetailData()) {// 明细数据的“其他”
			DetailRowData row = (DetailRowData) first;
			ArrayList<FieldCountDef> al_aggr = new ArrayList<FieldCountDef>();// 指标字段的统计设置
			ArrayList<Integer> al_idx = new ArrayList<Integer>(); // 指标字段的序号
			MemoryRowData data = new MemoryRowData(row.getMetaData(), null);
			Field[] flds = row.getMetaData().getFields();
			ElseField elseField = null;
//			List<ElseField> elseFields = topN.getElseFields() ;
//			FreeFieldConverter converter = m_areaModel.getAreaFields(false).getFieldConverter() ;
//			//改为从TopNInfo中循环查找
//			for (int i = 0; i < elseFields.size(); i++) {
//				ElseField elseField = elseFields.get(i) ;
//				String fieldName = converter.getConvertName(elseField.getFieldName()) ;
//				if(fieldName != null){
//					for (int j = 0; j < flds.length; j++) {
//						if(fieldName.equalsIgnoreCase(flds[j].getFldname())){
//							if(!elseField.isCount() && elseField.getShowName() != null){
//								data.setData(j, elseField.getShowName());
//							}else if(elseField.isCount()){
//								al_aggr.add(new FieldCountDef(flds[j], elseField.getCountType()));
//								al_idx.add(j);
//							}
//						}
//					}
//				}
//			}
			for (int i = 0; i < flds.length; i++) {
				elseField = getElseField(topN,flds[i].getFldname());
				if (elseField != null && !elseField.isCount() && elseField.getShowName() != null) {
					data.setData(i, elseField.getShowName());
				} else {

					// if (DataTypeConstant.isNumberType(flds[i].getDataType()))
					// if (flds[i].getExtType() != RptProvider.DIMENSION) {
					if (elseField != null && elseField.isCount()) {
						al_aggr.add(new FieldCountDef(flds[i], elseField.getCountType()));
						al_idx.add(i);
					} else {
						//没设的话，不再自动增加，完全按照topN设置对话框中的设置来设置 zhongkm
						/*if (DataTypeConstant.isNumberType(flds[i].getDataType())) {
							al_aggr.add(new FieldCountDef(flds[i], IFldCountType.TYPE_SUM));// 指标默认统计方式是sum，后续应该处理用户可设置
							al_idx.add(i);
						}*/
					}
					// }
				}
			}
			if (al_idx.size() > 0) {
				//增加唯一计数的处理
				Map<Integer, Set> coutDistinctMap = new HashMap<Integer, Set>();
				for (int i = begin; i < sortedRows.size(); i++) {
					row = (DetailRowData) sortedRows.get(i);//(DetailRowData) rowData.get(idx[i]);
					for (int j = 0; j < al_idx.size(); j++) {
						int m = al_idx.get(j);
						String fName = al_aggr.get(j).getMainFldName();
						Object rowValue = null;
						if (al_aggr.get(j).getCountType() == IFldCountType.TYPE_COUNT)
							rowValue = 1;
						else if (al_aggr.get(j).getCountType() == IFldCountType.TYPE_COUNT_DISTINCT) {// 唯一计数
							Object o = row.getData(fName);
							Set set = coutDistinctMap.get(j);
							if (set == null)
								set = new TreeSet();
							if (o != null && set.add(o)) {
								coutDistinctMap.put(j, set);
								rowValue = 1;
							} else
								rowValue = 0;
						} else
							rowValue = row.getData(fName);

						Object value = AnaDataSetTool.calcValue(data.getData(m), rowValue, al_aggr.get(j)
								.getCountType());
						data.setData(m, value);
					}					
				}
				coutDistinctMap.clear();
				int count = sortedRows.size() - begin;//idx.length - begin;
				for (int j = 0; j < al_idx.size(); j++) {// 对于平均数，进行除法
					int m = al_idx.get(j);
					Object dataValue = null;
					if (al_aggr.get(j).getCountType() == IFldCountType.TYPE_AVAGE) {
						dataValue = data.getData(m);
						if (dataValue != null)
							data.setData(m, (Double.parseDouble(dataValue.toString()) / count));
					}
				}
			}
			data.setGroupDatas(first.getGroupDatas());
			return data;
		} else {// 分组数据的“其他”
			GroupRowData row = new GroupRowData(grpDataSet, (GroupRowData) first,
					((GroupRowData) first).getGrpLvl() - 1);
			FieldCountDef count = fld.getFieldCountDef();
			FreeFieldConverter converter = m_areaModel.getAreaFields(false).getFieldConverter() ;
			if (count != null) {
				String grpFld = count.getRangeFldName();
				ElseField elseField = topN.getElseField(grpFld);
				if (elseField != null && !elseField.isCount() && elseField.getShowName() != null) {
					grpDataSet.setData(row, converter.getConvertName(grpFld), elseField.getShowName());
				}
			}else if(fld.getField() != null){
				String grpFld = fld.getField().getExpression();
				ElseField elseField = topN.getElseField(grpFld);
				if (elseField != null && !elseField.isCount() && elseField.getShowName() != null) {
					grpDataSet.setData(row, converter.getConvertName(grpFld), elseField.getShowName());
				}
			}
			for (int i = begin; i < sortedRows.size(); i++) {
				row = m_areaModel.getDSTool().appendAggrData(grpDataSet, (GroupRowData) row, sortedRows.get(i),false);//rowData.get(idx[i]), false);
			}
			return row;
		}
	}

	private AbsRowData createNullElseRow(GroupDataSet grpDataSet, AbsRowData row, AnaRepField fld) {
		if(row == null)
			return createNullRow(grpDataSet, row, 1);

		TopNSetInfo topN = (TopNSetInfo) fld.getTopNInfo();
		if (row.isDetailData()) {// 明细数据的“其他”
			MemoryRowData data = new MemoryRowData(row.getMetaData(), null);
			Field[] flds = row.getMetaData().getFields();
			ElseField elseField = null;
			for (int i = 0; i < flds.length; i++) {
				elseField = getElseField(topN,flds[i].getFldname());
				if (elseField != null && !elseField.isCount() && elseField.getShowName() != null) {
					data.setData(i, elseField.getShowName());
				}
			}
			return data;
		} else {// 分组数据的“其他”
			GroupRowData data = new GroupRowData(grpDataSet, (GroupRowData) row,
					((GroupRowData) row).getGrpLvl() - 1);
			FieldCountDef count = fld.getFieldCountDef();
			if (count != null) {
				String grpFld = count.getRangeFldName();
				ElseField elseField = topN.getElseField(grpFld);
				FreeFieldConverter converter = m_areaModel.getAreaFields(false).getFieldConverter() ;
				if (elseField != null && !elseField.isCount() && elseField.getShowName() != null) {
					grpDataSet.setData(data, converter.getConvertName(grpFld), elseField.getShowName());
				}
			}
			return data;
		}
	}
	//通过别名查找
	private ElseField getElseField(TopNSetInfo topN,String fldName){
		List<ElseField> elseFields = topN.getElseFields() ;
		FreeFieldConverter converter = m_areaModel.getAreaFields(false).getFieldConverter() ;
		for (int i = 0; i < elseFields.size(); i++) {
			ElseField elseField = elseFields.get(i) ;
			String fieldName = converter.getConvertName(elseField.getFieldName()) ;
			if(fieldName != null && fieldName.equalsIgnoreCase(fldName)){
				return elseField ;
			}
		}
		return null ;
	}
}
