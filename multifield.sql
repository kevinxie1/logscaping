alter table VENDOR_MAPPING add SCHEMAID_tmp varchar2(4000);
update VENDOR_MAPPING set SCHEMAID_tmp = SCHEMAID;
commit;
alter table VENDOR_MAPPING drop column SCHEMAID;
alter table VENDOR_MAPPING rename column SCHEMAID_tmp to SCHEMAID;

alter table VENDOR_MAPPING add FIELDID_tmp varchar2(4000);
update VENDOR_MAPPING set FIELDID_tmp = FIELDID;
commit;
alter table VENDOR_MAPPING drop column FIELDID;
alter table VENDOR_MAPPING rename column FIELDID_tmp to FIELDID;

alter table VENDOR_MAPPING add OVERLAYGROUP_tmp varchar2(4000);
update VENDOR_MAPPING set OVERLAYGROUP_tmp = OVERLAYGROUP;
commit;
alter table VENDOR_MAPPING drop column OVERLAYGROUP;
alter table VENDOR_MAPPING rename column OVERLAYGROUP_tmp to OVERLAYGROUP;

alter table VIEW_MAPPING add SCHEMAID_tmp varchar2(4000);
update VIEW_MAPPING set SCHEMAID_tmp = SCHEMAID;
commit;
alter table VIEW_MAPPING drop column SCHEMAID;
alter table VIEW_MAPPING rename column SCHEMAID_tmp to SCHEMAID;

alter table VIEW_MAPPING add FIELDID_tmp varchar2(4000);
update VIEW_MAPPING set FIELDID_tmp = FIELDID;
commit;
alter table VIEW_MAPPING drop column FIELDID;
alter table VIEW_MAPPING rename column FIELDID_tmp to FIELDID;

alter table VIEW_MAPPING add OVERLAYGROUP_tmp varchar2(4000);
update VIEW_MAPPING set OVERLAYGROUP_tmp = OVERLAYGROUP;
commit;
alter table VIEW_MAPPING drop column OVERLAYGROUP;
alter table VIEW_MAPPING rename column OVERLAYGROUP_tmp to OVERLAYGROUP;

alter table VIEW_PERMISSIONS add VIEWMETADATAID_tmp varchar2(4000);
update VIEW_PERMISSIONS set VIEWMETADATAID_tmp = VIEWMETADATAID;
commit;
alter table VIEW_PERMISSIONS drop column VIEWMETADATAID;
alter table VIEW_PERMISSIONS rename column VIEWMETADATAID_tmp to VIEWMETADATAID;

alter table VIEW_PERMISSIONS add GROUPID_tmp varchar2(4000);
update VIEW_PERMISSIONS set GROUPID_tmp = GROUPID;
commit;
alter table VIEW_PERMISSIONS drop column GROUPID;
alter table VIEW_PERMISSIONS rename column GROUPID_tmp to GROUPID;

alter table VIEW_PERMISSIONS add OVERLAYGROUP_tmp varchar2(4000);
update VIEW_PERMISSIONS set OVERLAYGROUP_tmp = OVERLAYGROUP;
commit;
alter table VIEW_PERMISSIONS drop column OVERLAYGROUP;
alter table VIEW_PERMISSIONS rename column OVERLAYGROUP_tmp to OVERLAYGROUP;

alter table VIEWCOMPONENT add GUID_tmp varchar2(4000);
update VIEWCOMPONENT set GUID_tmp = GUID;
commit;
alter table VIEWCOMPONENT drop column GUID;
alter table VIEWCOMPONENT rename column GUID_tmp to GUID;

alter table VIEWCOMPONENT add OVERLAYGROUP_tmp varchar2(4000);
update VIEWCOMPONENT set OVERLAYGROUP_tmp = OVERLAYGROUP;
commit;
alter table VIEWCOMPONENT drop column OVERLAYGROUP;
alter table VIEWCOMPONENT rename column OVERLAYGROUP_tmp to OVERLAYGROUP;

alter table VIEWCOMPONENT_PERMISSIONS add GUID_tmp varchar2(4000);
update VIEWCOMPONENT_PERMISSIONS set GUID_tmp = GUID;
commit;
alter table VIEWCOMPONENT_PERMISSIONS drop column GUID;
alter table VIEWCOMPONENT_PERMISSIONS rename column GUID_tmp to GUID;

alter table VIEWCOMPONENT_PERMISSIONS add GROUPID_tmp varchar2(4000);
update VIEWCOMPONENT_PERMISSIONS set GROUPID_tmp = GROUPID;
commit;
alter table VIEWCOMPONENT_PERMISSIONS drop column GROUPID;
alter table VIEWCOMPONENT_PERMISSIONS rename column GROUPID_tmp to GROUPID;

alter table VIEWCOMPONENT_PERMISSIONS add OVERLAYGROUP_tmp varchar2(4000);
update VIEWCOMPONENT_PERMISSIONS set OVERLAYGROUP_tmp = OVERLAYGROUP;
commit;
alter table VIEWCOMPONENT_PERMISSIONS drop column OVERLAYGROUP;
alter table VIEWCOMPONENT_PERMISSIONS rename column OVERLAYGROUP_tmp to OVERLAYGROUP;

alter table VIEWS add VIEWMETADATAID_tmp varchar2(4000);
update VIEWS set VIEWMETADATAID_tmp = VIEWMETADATAID;
commit;
alter table VIEWS drop column VIEWMETADATAID;
alter table VIEWS rename column VIEWMETADATAID_tmp to VIEWMETADATAID;

alter table VIEWS add OVERLAYGROUP_tmp varchar2(4000);
update VIEWS set OVERLAYGROUP_tmp = OVERLAYGROUP;
commit;
alter table VIEWS drop column OVERLAYGROUP;
alter table VIEWS rename column OVERLAYGROUP_tmp to OVERLAYGROUP;

alter table VUI add SCHEMAID_tmp varchar2(4000);
update VUI set SCHEMAID_tmp = SCHEMAID;
commit;
alter table VUI drop column SCHEMAID;
alter table VUI rename column SCHEMAID_tmp to SCHEMAID;

alter table VUI add VUIID_tmp varchar2(4000);
update VUI set VUIID_tmp = VUIID;
commit;
alter table VUI drop column VUIID;
alter table VUI rename column VUIID_tmp to VUIID;

alter table VUI add OVERLAYGROUP_tmp varchar2(4000);
update VUI set OVERLAYGROUP_tmp = OVERLAYGROUP;
commit;
alter table VUI drop column OVERLAYGROUP;
alter table VUI rename column OVERLAYGROUP_tmp to OVERLAYGROUP;

