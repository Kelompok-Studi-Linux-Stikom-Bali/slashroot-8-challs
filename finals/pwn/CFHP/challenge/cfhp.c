#include "qemu/osdep.h"
#include "hw/pci/pci_device.h"
#include "hw/qdev-properties.h"
#include "qemu/module.h"
#include "qom/object.h"
#include "qemu/module.h"
#include "qemu/units.h"
#include "qapi/visitor.h"
#include "hw/hw.h"
#include "hw/pci/msi.h"
#include "hw/pci/pci.h"
#include "sysemu/dma.h"

#define TYPE_PCI_CFHP_DEV "cfhp"

#define CFHP_MMIO_SRC 0x10
#define CFHP_MMIO_DST 0x20
#define CFHP_MMIO_SZ 0x30
#define CFHP_MMIO_OP 0x40
#define CFHP_MMIO_EXEC 0x50
#define DMA_READ 0
#define DMA_WRITE 1

struct CFHPDevState {
    PCIDevice parent_obj;
    MemoryRegion mmio;
    AddressSpace *addr;

    struct DMAState {
        dma_addr_t src;
        dma_addr_t dst;
        dma_addr_t sz;
    } dma;

    char buff[0x1000];
};

OBJECT_DECLARE_SIMPLE_TYPE(CFHPDevState, PCI_CFHP_DEV);

static bool cfhp_dma_exec(CFHPDevState *cfhp, int rw) {
    //PCIDevice *pdev = PCI_DEVICE(cfhp);
    switch (rw) {
        case DMA_READ:
            dma_memory_write(cfhp->addr, cfhp->dma.dst, cfhp->buff + cfhp->dma.src, cfhp->dma.sz, MEMTXATTRS_UNSPECIFIED);
            //pci_dma_write(pdev, cfhp->dma.dst, cfhp->buff + cfhp->dma.src, cfhp->dma.sz);
            break;
        case DMA_WRITE:
            dma_memory_read(cfhp->addr, cfhp->dma.src, cfhp->buff + cfhp->dma.dst, cfhp->dma.sz, MEMTXATTRS_UNSPECIFIED);
            //pci_dma_read(pdev, cfhp->dma.src, cfhp->buff + cfhp->dma.dst, cfhp->dma.sz);
            break;
        default:
            return false;
    }
    return true;
}

static uint64_t cfhp_mmio_read(void *opaque, hwaddr addr, unsigned size) {
    CFHPDevState *cfhp = opaque;
    uint64_t val = 0;
    switch (addr) {
        case CFHP_MMIO_SRC:
            val = cfhp->dma.src;
            break;
        case CFHP_MMIO_DST:
            val = cfhp->dma.dst;
            break;
        case CFHP_MMIO_SZ:
            val = cfhp->dma.sz;
            break;
        case CFHP_MMIO_EXEC:
            val = cfhp_dma_exec(cfhp, DMA_READ);
            break;
        default:
            val = 0xDEADC0DE;
            break;
    }
    return val;
}

static void cfhp_mmio_write(void *opaque, hwaddr addr, uint64_t val, unsigned size){
    CFHPDevState *cfhp = opaque;
    switch (addr) {
        case CFHP_MMIO_SRC:
            cfhp->dma.src = val;
            break;
        case CFHP_MMIO_DST:
            cfhp->dma.dst = val;
            break;
        case CFHP_MMIO_SZ:
            cfhp->dma.sz = val;
            break;
        case CFHP_MMIO_EXEC:
            cfhp_dma_exec(cfhp, DMA_WRITE);
            break;
        default:
            break;
    }
    return;
}

static const MemoryRegionOps cfhp_mmio_ops = {
    .read = cfhp_mmio_read,
    .write = cfhp_mmio_write,
    .endianness = DEVICE_NATIVE_ENDIAN,
    .valid = {
        .min_access_size = 4,
        .max_access_size = 8,
    },
    .impl = {
        .min_access_size = 4,
        .max_access_size = 8,
    },
};

static void cfhp_dev_realize(PCIDevice *pdev, Error **errp) {
    CFHPDevState *cfhp = PCI_CFHP_DEV(pdev);
    if (msi_init(pdev, 0, 1, true, false, errp)) return;
    cfhp->addr = &address_space_memory;
    memory_region_init_io(&cfhp->mmio, OBJECT(cfhp), &cfhp_mmio_ops, cfhp, "cfhp-mmio", 0x1000);
    pci_register_bar(pdev, 0, PCI_BASE_ADDRESS_SPACE_MEMORY, &cfhp->mmio);
}

static void cfhp_instance_init(Object *obj) {}
static void pci_cfhp_exit(PCIDevice *pdev) {
    msi_uninit(pdev);
}

static void cfhp_class_init(ObjectClass *class, void *data) {
    DeviceClass *dc = DEVICE_CLASS(class);
    PCIDeviceClass *k = PCI_DEVICE_CLASS(class);
    k->realize = cfhp_dev_realize;
    k->exit = pci_cfhp_exit;
    k->vendor_id = 0xf0f0;
    k->device_id = 0xf4f4;
    k->revision = 0x69;
    k->class_id = PCI_CLASS_OTHERS;
    set_bit(DEVICE_CATEGORY_MISC, dc->categories);
}

static const TypeInfo cfhp_info = {
    .name = TYPE_PCI_CFHP_DEV,
    .parent = TYPE_PCI_DEVICE,
    .instance_size = sizeof(CFHPDevState),
    .class_init = cfhp_class_init,
    .instance_init = cfhp_instance_init,
    .interfaces = (InterfaceInfo[]) {
        { INTERFACE_CONVENTIONAL_PCI_DEVICE },
        { }
    },
};

static void pci_cfhp_register_types(void){
    type_register_static(&cfhp_info);
}

type_init(pci_cfhp_register_types)
